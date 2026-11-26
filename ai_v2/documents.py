"""Download (once, addressed by sha256), validation and rendering of label files.

- size and page limits (safety + cost);
- file type detected from its signature (magic bytes), never from the extension;
- PDF: text layer (pypdf) + pages rendered as PNG (pypdfium2) for the vision model;
- images: normalised (RGB, longest side capped);
- one perceptual fingerprint (dHash) per page, to spot the same artwork reused across declarations.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import io
import json
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from PIL import Image

from .config import Settings

Image.MAX_IMAGE_PIXELS = 120_000_000  # guard against decompression bombs


class DocumentError(RuntimeError):
    """The FILE itself is the problem (unknown format, corrupt, too large). Can justify a finding,
    unlike a network or API failure, which only ever leads to an ERROR to be replayed."""


@dataclass
class Page:
    index: int
    png_path: Path
    width: int
    height: int
    text_layer: str = ""  # embedded PDF text, independent of the page orientation
    dhash: str = ""


@dataclass
class LabelDocument:
    url: str
    sha256: str
    kind: str  # pdf | image
    path: Path
    n_pages_total: int
    pages: list[Page] = field(default_factory=list)  # rendered pages (at most max_pages_per_file)

    def page_data_url(
        self, i: int, crop: tuple[float, float, float, float] | None = None, max_side: int = 1600, rotation: int = 0
    ) -> str:
        """Page `i` as a JPEG data URL for the vision model, optionally rotated and cropped.

        `crop` is (x0, y0, x1, y1) in fractions of the page (used by the agent to zoom on a zone).
        """
        img = Image.open(self.pages[i].png_path)
        if rotation:
            img = img.rotate(-rotation, expand=True)  # clockwise, in degrees
        if crop:
            x0, y0, x1, y1 = crop
            w, h = img.size
            img = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
        img.thumbnail((max_side, max_side))
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=88)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

    @property
    def text_layer(self) -> str:
        return "\n".join(p.text_layer for p in self.pages)

    def ocr_tiles(self, i: int, grid: int = 2, long_side: int = 4000, overlap: float = 0.08) -> list[str]:
        """Page `i` in HIGH resolution, cut into grid x grid overlapping tiles, for small-print OCR.

        Needed when the label is an image embedded in a PDF: "document" OCR then returns the image
        without reading the text inside it. Tiles are returned as JPEG data URLs.
        """
        if self.kind == "pdf":
            import pypdfium2 as pdfium

            pdf = pdfium.PdfDocument(str(self.path))
            page = pdf[i]
            w_pt, h_pt = page.get_size()
            img = page.render(scale=long_side / max(w_pt, h_pt, 1)).to_pil().convert("RGB")
            pdf.close()
        else:
            img = Image.open(self.path).convert("RGB")
            if max(img.size) > long_side:
                img.thumbnail((long_side, long_side))
        W, H = img.size
        out = []
        for gx in range(grid):
            for gy in range(grid):
                x0 = max(0, int((gx / grid - overlap) * W))
                x1 = min(W, int(((gx + 1) / grid + overlap) * W))
                y0 = max(0, int((gy / grid - overlap) * H))
                y1 = min(H, int(((gy + 1) / grid + overlap) * H))
                tile = img.crop((x0, y0, x1, y1))
                tile.thumbnail((2200, 2200))
                buf = io.BytesIO()
                tile.save(buf, format="JPEG", quality=90)
                out.append("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
        return out


def _sniff(data: bytes) -> str:
    """'pdf' or 'image' from the file's magic bytes; DocumentError for anything else."""
    if data[:5] == b"%PDF-":
        return "pdf"
    if data[:8] == b"\x89PNG\r\n\x1a\n" or data[:3] == b"\xff\xd8\xff" or data[:4] == b"RIFF" or data[:3] == b"GIF":
        return "image"
    raise DocumentError("unrecognised file format (neither PDF nor image)")


def dhash(img: Image.Image, size: int = 8) -> str:
    """64-bit difference hash: robust to resizing and recompression, compared by Hamming distance."""
    g = img.convert("L").resize((size + 1, size), Image.Resampling.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for row in range(size):
        for col in range(size):
            left = px[row * (size + 1) + col]
            right = px[row * (size + 1) + col + 1]
            bits = (bits << 1) | (1 if left > right else 0)
    return f"{bits:016x}"


class DocumentStore:
    """Local store of label files: <data_dir>/files/<sha256>.<ext>, plus rendered pages and metadata."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.root = settings.data_dir / "files"
        self.root.mkdir(parents=True, exist_ok=True)
        # url -> sha256, so that a file already downloaded is never fetched again
        self.url_index_path = self.root / "url_index.json"
        self._url_index: dict[str, str] = (
            json.loads(self.url_index_path.read_text(encoding="utf-8")) if self.url_index_path.exists() else {}
        )
        self._lock = asyncio.Lock()
        self._http = httpx.AsyncClient(timeout=httpx.Timeout(60, connect=20), follow_redirects=True)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def _download(self, url: str) -> tuple[str, Path]:
        if url in self._url_index:
            sha = self._url_index[url]
            found = list(self.root.glob(f"{sha}.*"))
            if found:
                return sha, found[0]
        # Streamed, so that an oversized file is rejected without being fully downloaded.
        chunks, size = [], 0
        async with self._http.stream("GET", url) as resp:
            if resp.status_code != 200:
                raise DocumentError(f"download failed: HTTP {resp.status_code}")
            async for chunk in resp.aiter_bytes():
                size += len(chunk)
                if size > self.settings.max_file_bytes:
                    raise DocumentError(f"file too large (> {self.settings.max_file_bytes // 1_000_000} MB)")
                chunks.append(chunk)
        data = b"".join(chunks)
        kind = _sniff(data)
        sha = hashlib.sha256(data).hexdigest()
        path = self.root / f"{sha}.{'pdf' if kind == 'pdf' else 'img'}"
        if not path.exists():
            path.write_bytes(data)
        async with self._lock:
            self._url_index[url] = sha
            self.url_index_path.write_text(json.dumps(self._url_index), encoding="utf-8")
        return sha, path

    async def load(self, url: str) -> LabelDocument:
        sha, path = await self._download(url)
        return await asyncio.to_thread(self._render, url, sha, path)

    def _render(self, url: str, sha: str, path: Path) -> LabelDocument:
        """Render the pages once; later calls reuse <files>/pages/<sha>/meta.json."""
        s = self.settings
        out_dir = self.root / "pages" / sha
        out_dir.mkdir(parents=True, exist_ok=True)
        meta_path = out_dir / "meta.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            pages = [
                Page(
                    index=p["index"],
                    png_path=out_dir / p["file"],
                    width=p["width"],
                    height=p["height"],
                    text_layer=p["text_layer"],
                    dhash=p["dhash"],
                )
                for p in meta["pages"]
            ]
            return LabelDocument(
                url=url, sha256=sha, kind=meta["kind"], path=path, n_pages_total=meta["n_pages_total"], pages=pages
            )

        kind = "pdf" if path.suffix == ".pdf" else "image"
        pages: list[Page] = []
        if kind == "pdf":
            import pypdfium2 as pdfium
            from pypdf import PdfReader

            texts: list[str] = []
            try:
                reader = PdfReader(str(path))
                for i, pg in enumerate(reader.pages[: s.max_pages_per_file]):
                    try:
                        texts.append(pg.extract_text() or "")
                    except Exception:  # noqa: BLE001 - one unreadable page must not break the file
                        texts.append("")
            except Exception:  # noqa: BLE001
                texts = []
            pdf = pdfium.PdfDocument(str(path))
            n_total = len(pdf)
            for i in range(min(n_total, s.max_pages_per_file)):
                page = pdf[i]
                w_pt, h_pt = page.get_size()
                # render_dpi, but never more than max_image_side pixels on the longest side
                scale = min(s.render_dpi / 72, s.max_image_side / max(w_pt, h_pt, 1))
                img = page.render(scale=max(scale, 0.5)).to_pil().convert("RGB")
                f = f"p{i}.png"
                img.save(out_dir / f, optimize=True)
                pages.append(
                    Page(
                        index=i,
                        png_path=out_dir / f,
                        width=img.width,
                        height=img.height,
                        text_layer=texts[i] if i < len(texts) else "",
                        dhash=dhash(img),
                    )
                )
            pdf.close()
        else:
            img = Image.open(path)
            img = img.convert("RGB")
            img.thumbnail((s.max_image_side, s.max_image_side))
            img.save(out_dir / "p0.png", optimize=True)
            n_total = 1
            pages.append(
                Page(index=0, png_path=out_dir / "p0.png", width=img.width, height=img.height, dhash=dhash(img))
            )

        meta = {
            "kind": kind,
            "n_pages_total": n_total,
            "pages": [
                {
                    "index": p.index,
                    "file": p.png_path.name,
                    "width": p.width,
                    "height": p.height,
                    "text_layer": p.text_layer,
                    "dhash": p.dhash,
                }
                for p in pages
            ],
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        return LabelDocument(url=url, sha256=sha, kind=kind, path=path, n_pages_total=n_total, pages=pages)
