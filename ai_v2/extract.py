"""Stages 1-2: OCR (once, cached) + structured extraction by a vision model.

The extraction is done BLIND (the model never sees the declaration) to avoid confirmation bias;
the comparison with the declaration happens afterwards, in code (rules.py). Every quote is then
"grounded": we check that it really exists in the OCR transcript or in the PDF text layer.

The OCR text and the instructions sent to the model are in French, like the labels: they are
model input, and changing them invalidates the cached extractions.
"""

from __future__ import annotations

import asyncio
import re

from pydantic import BaseModel, Field

from .cache import stable_hash
from .config import Settings, prompt_hash, prompt_text
from .documents import LabelDocument
from .llm import LLMClient, LLMError
from .schemas import SCHEMA_VERSION, LabelExtraction, Mention, MentionStatus
from .text import normalise, quote_in_text

# Minimum quote_in_text score for a quote to count as found in the label text.
GROUNDING_THRESHOLD = 80.0
# Pages sent as images to the vision model (the OCR text covers up to max_pages_per_file).
MAX_VLM_PAGES = 3


class FileExtraction(BaseModel):
    """Everything known about one label file after stages 1-2."""

    url: str
    sha256: str
    kind: str
    n_pages_total: int
    ocr_pages: list[str]
    extraction: LabelExtraction
    grounding: dict = Field(default_factory=dict)
    # PDF text layer: independent of the orientation (it reads blocks printed upside down)
    text_layer: str = ""

    @property
    def full_text(self) -> str:
        return "\n".join(self.ocr_pages) + ("\n" + self.text_layer if self.text_layer else "")


def grounded(quote: str | None, text: str) -> bool:
    return quote_in_text(quote, text) >= GROUNDING_THRESHOLD


async def _ocr_pages(client: LLMClient, settings: Settings, doc: LabelDocument) -> list[str]:
    try:
        ocr = await client.ocr(doc.url, doc.kind == "pdf", doc.sha256, settings.max_pages_per_file)
        return [p["markdown"] for p in ocr["pages"]]
    except LLMError as e:
        if "HTTP 400" not in str(e):
            raise
        # e.g. "image too large": OCR our own rendered (and downscaled) pages instead, one by one
        return list(
            await asyncio.gather(
                *(
                    client.ocr_image(doc.page_data_url(i, max_side=2000), f"{doc.sha256}:p{i}:r0")
                    for i in range(len(doc.pages))
                )
            )
        )


async def ocr_rotated(client: LLMClient, doc: LabelDocument) -> str:
    """OCR of every page turned by 90, 180 and 270 degrees: text printed sideways or upside down
    (common for the French block of multilingual labels) is invisible to upright OCR.

    Only called when a mandatory statement looks absent, before concluding that it is.
    """
    jobs = [
        client.ocr_image(doc.page_data_url(i, max_side=2000, rotation=rot), f"{doc.sha256}:p{i}:r{rot}")
        for i in range(len(doc.pages))
        for rot in (90, 180, 270)
    ]
    return "\n".join(await asyncio.gather(*jobs))


# Markdown image links the OCR leaves in its output ("![img-0.jpeg](img-0.jpeg)"): not label text.
IMAGE_LINK = re.compile(r"!\[[^\]]*\]\([^)]*\)")
# Below this many characters on a page, we assume the OCR missed text (label embedded as an image).
MIN_TEXT_PER_PAGE = 1500


async def _densify(client: LLMClient, doc: LabelDocument, ocr_pages: list[str]) -> tuple[list[str], int]:
    """Re-read, in high resolution and by tiles, the pages where the OCR found little text
    (label embedded as an image, small print). Returns (enriched pages, number of pages re-read)."""
    out, n = list(ocr_pages), 0
    if doc.kind == "image":
        from PIL import Image

        size = await asyncio.to_thread(lambda: Image.open(doc.path).size)
        if max(size) <= 3000:  # the OCR already read the image at full resolution
            return out, 0
    for i in range(len(doc.pages)):
        ocr_text = IMAGE_LINK.sub("", out[i]) if i < len(out) else ""
        layer = doc.pages[i].text_layer if doc.kind == "pdf" else ""
        if len(ocr_text.strip()) >= MIN_TEXT_PER_PAGE or len(normalise(layer)) >= MIN_TEXT_PER_PAGE:
            continue
        tiles = await asyncio.to_thread(doc.ocr_tiles, i)
        texts = await asyncio.gather(
            *(client.ocr_image(t, f"{doc.sha256}:p{i}:tile{k}:v1") for k, t in enumerate(tiles))
        )
        extra = "\n".join(texts)
        # The marker below is part of the extraction input (and of its cache key): keep it unchanged.
        if i < len(out):
            out[i] = out[i] + "\n\n[Relecture haute résolution par tuiles]\n" + extra
        else:
            out.append(extra)
        n += 1
    return out, n


async def extract_document(client: LLMClient, settings: Settings, doc: LabelDocument) -> FileExtraction:
    """OCR + densification + blind structured extraction of one label file, then grounding."""
    ocr_pages = await _ocr_pages(client, settings, doc)
    ocr_pages, densified = await _densify(client, doc, ocr_pages)
    transcript = "\n\n".join(f"=== Page {i} ===\n{t}" for i, t in enumerate(ocr_pages))
    if doc.kind == "pdf" and normalise(doc.text_layer):
        transcript += "\n\n=== Couche texte du PDF (si différente) ===\n" + doc.text_layer[:20000]

    # The model gets both the OCR transcript and the page images: the text helps with small print,
    # the images let it correct OCR errors and understand the layout.
    content: list[dict] = [
        {
            "type": "text",
            "text": "Transcription OCR automatique (peut contenir des erreurs) :\n\n" + transcript[:60000],
        }
    ]
    for i, _ in enumerate(doc.pages[:MAX_VLM_PAGES]):
        content.append({"type": "text", "text": f"Image de la page {i} :"})
        content.append({"type": "image_url", "image_url": doc.page_data_url(i, max_side=1536)})
    content.append({"type": "text", "text": "Extrais les faits de cette étiquette selon le schéma."})

    messages = [
        {"role": "system", "content": prompt_text("extract_label.md")},
        {"role": "user", "content": content},
    ]
    cache_parts = {
        "file": doc.sha256,
        "ocr_model": settings.model_ocr,
        "prompt": prompt_hash("extract_label.md"),
        "schema": SCHEMA_VERSION,
        "pages": len(doc.pages[:MAX_VLM_PAGES]),
    }
    if densified:  # the transcript changed: new extraction (the other files stay cached)
        cache_parts["ocr_tiles"] = stable_hash(ocr_pages)
    extraction: LabelExtraction = await client.chat_json(
        "extract",
        settings.model_extract,
        messages,
        LabelExtraction,
        max_tokens=16000,
        cache_parts=cache_parts,
    )
    fe = FileExtraction(
        url=doc.url,
        sha256=doc.sha256,
        kind=doc.kind,
        n_pages_total=doc.n_pages_total,
        ocr_pages=ocr_pages,
        extraction=extraction,
        text_layer=doc.text_layer[:40000],
    )
    fe.grounding = grounding_report(fe)
    return fe


def grounding_report(fe: FileExtraction, text_layer: str = "") -> dict:
    """Which extracted items can be found again in the label text. The *_flags lists are aligned
    with extraction.ingredients / extraction.composition and drive LabelRow.grounded."""
    text = fe.full_text + "\n" + text_layer
    ex = fe.extraction
    ing = [grounded(i.raw, text) for i in ex.ingredients]
    comp = [grounded(c.raw, text) for c in ex.composition]
    mentions = {k: grounded(m.quote, text) for k, m in ex.mentions if m.status == MentionStatus.present}
    return {
        "ingredients_grounded": sum(ing),
        "ingredients_total": len(ing),
        "ingredient_flags": ing,
        "composition_grounded": sum(comp),
        "composition_total": len(comp),
        "composition_flags": comp,
        "mentions_present_grounded": mentions,
        "ocr_chars": len(fe.full_text),
    }


# ---------------------------------------------------------------------------------------- merge
class MergedLabel(BaseModel):
    """All label files of a declaration seen as one label (a declaration can attach several files)."""

    files: list[FileExtraction]
    extra_text: str = ""  # OCR of the rotated pages (text printed sideways)

    @property
    def text(self) -> str:
        """All the label text we have: OCR of every file, PDF text layers and rotated OCR."""
        return "\n".join(f.full_text for f in self.files) + ("\n" + self.extra_text if self.extra_text else "")

    def ingredients(self):
        """(file index, ingredient, grounded) tuples, de-duplicated on (normalised name, plant part)."""
        seen, out = set(), []
        for fi, f in enumerate(self.files):
            for i, ing in enumerate(f.extraction.ingredients):
                k = (normalise(ing.botanical_name or ing.name), normalise(ing.plant_part))
                if k in seen or not normalise(ing.name):
                    continue
                seen.add(k)
                out.append((fi, ing, f.grounding.get("ingredient_flags", [True] * 999)[i]))
        return out

    def composition(self):
        """(file index, composition row, grounded) tuples, de-duplicated on (name, value, unit)."""
        seen, out = set(), []
        for fi, f in enumerate(self.files):
            for i, row in enumerate(f.extraction.composition):
                k = (normalise(row.name), row.value, normalise(row.unit))
                if k in seen:
                    continue
                seen.add(k)
                out.append((fi, row, f.grounding.get("composition_flags", [True] * 999)[i]))
        return out

    def mention(self, key: str) -> tuple[Mention, int | None]:
        """Best status of a mandatory statement across files (present > unclear > absent)."""
        best, best_fi = None, None
        rank = {MentionStatus.present: 2, MentionStatus.unclear: 1, MentionStatus.absent: 0}
        for fi, f in enumerate(self.files):
            m: Mention = getattr(f.extraction.mentions, key)
            if best is None or rank[m.status] > rank[best.status]:
                best, best_fi = m, fi
        return best, best_fi

    def first(self, getter):
        """First truthy value of getter(extraction) across files, else None."""
        for f in self.files:
            v = getter(f.extraction)
            if v:
                return v
        return None

    def warnings(self):
        return [(fi, w) for fi, f in enumerate(self.files) for w in f.extraction.warnings]

    def claims(self):
        return [(fi, c) for fi, f in enumerate(self.files) for c in f.extraction.claims]
