"""Central configuration: pinned models, prices, limits and decision thresholds.

Everything that can change a result lives here and is copied into each run's manifest
(`runs.RunStore.write_manifest`), so that two runs can always be compared.

Nothing secret or environment-specific is hard-coded: the database, the media bucket and the
Mistral key come from environment variables, or from a local, untracked env file (`KEY_FILES`).
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = PACKAGE_DIR / "prompts"

# Durable data folder (cache, downloaded files, runs, gold datasets). It lives OUTSIDE the repo
# because it contains production data (labels, declarations, instructor comments).
DEFAULT_DATA_DIR = Path(os.environ.get("AI_V2_DATA_DIR", PACKAGE_DIR.parent.parent / "ai_v2_data"))

# Local env files, read line by line as `NAME=value`. They hold the Mistral key and the private
# settings below; they are never printed or logged, and must never be committed.
KEY_FILES = [
    Path.home() / ".complalim" / "ai_v2.env",
    PACKAGE_DIR.parent.parent / "ai_v2.env",
    PACKAGE_DIR.parent.parent / "ai_v2.env.txt",
]


def _read_key(name: str) -> str | None:
    """Return `name` from the environment, else from the first env file that defines it."""
    if os.environ.get(name):
        return os.environ[name].strip()
    for path in KEY_FILES:
        if path.exists():
            for line in path.read_text(encoding="utf-8-sig").splitlines():
                if line.strip().startswith(f"{name}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


# Base URL of the media bucket, ending with "/". Label files are public (the app sets
# AWS_QUERYSTRING_AUTH = False in config/settings.py), so no credentials are needed to download them.
MEDIA_BASE_URL = _read_key("AI_V2_MEDIA_BASE_URL") or ""


@dataclass(frozen=True)
class ModelPrice:
    """Price of a model, in USD per million tokens (or per 1,000 pages for OCR)."""

    input_per_m: float = 0.0
    output_per_m: float = 0.0
    cached_input_per_m: float = 0.0
    per_1000_pages: float = 0.0


# Public prices as of November 2026 (secondary sources: reconcile with the invoice).
# Deliberately on the high side, because the budget guard (llm.client.Usage) relies on them.
PRICES: dict[str, ModelPrice] = {
    "mistral-medium-3-5": ModelPrice(1.50, 7.50, 0.15),
    "mistral-large-4-0": ModelPrice(2.00, 8.00, 0.20),
    "mistral-small-2603": ModelPrice(0.20, 0.60, 0.02),
    "mistral-embed-2312": ModelPrice(0.10, 0.0),
    "mistral-ocr-4-1": ModelPrice(per_1000_pages=4.0),
}


@dataclass
class Settings:
    data_dir: Path = DEFAULT_DATA_DIR
    media_base_url: str = MEDIA_BASE_URL

    # --- Database (read-only, enforced server-side: see db.py) ---
    db_server: str = field(default_factory=lambda: os.environ.get("db_server", ""))  # "host:port"
    db_user: str = field(default_factory=lambda: os.environ.get("db_user", ""))
    db_name: str = field(default_factory=lambda: _read_key("db_name") or "")

    # --- Pinned models (never *-latest: a run must be reproducible) ---
    model_ocr: str = "mistral-ocr-4-1"
    model_extract: str = "mistral-medium-3-5"  # vision + structured output
    model_resolve: str = "mistral-small-2603"  # picks one ID among candidates
    model_check: str = "mistral-small-2603"  # short semantic checks (warnings)
    model_agent: str = "mistral-medium-3-5"  # verification agent with tools
    model_embed: str = "mistral-embed-2312"
    model_gold: str = "mistral-small-2603"  # structures instructor comments (gold set)

    # --- Concurrency / robustness (account limits: 2,000 req/min and 2M tokens/min per model) ---
    max_concurrent_declarations: int = 8
    max_concurrent_llm_calls: int = 12
    requests_per_second: float = 15.0
    max_retries: int = 6
    request_timeout_s: float = 180.0

    # --- Document limits (safety + cost) ---
    max_file_bytes: int = 30 * 1024 * 1024
    max_pages_per_file: int = 6
    max_label_files: int = 4
    render_dpi: int = 160
    max_image_side: int = 2000

    # --- Budget: the run stops cleanly when the estimated spend reaches this amount ---
    budget_usd: float = 30.0

    # --- Verification agent ---
    agent_max_turns: int = 10
    agent_enabled: bool = True

    # --- Decision policy (see decision.is_blocking) ---
    # BLOCK if a BLOCKING finding reaches this confidence (after verification) and is proven...
    block_confidence: float = 0.80
    # ... or if the aggregated risk score (noisy-OR, decision.risk_score) exceeds this threshold...
    block_risk_score: float = 0.97
    # ... or if a MAJOR finding from one of these code families is confirmed, with proof, by the agent.
    # Calibrated on run 20261120-173156_gold_v1_v5 (eval/policy.py, adjudicated ground truth):
    #   doses + warnings: precision 93 %, recall 51 %  <- default ("be sure before blocking")
    #   + mentions (art. 12-I quantities, drops -> ml...): precision 84 %, recall 73 %. That one is a
    #     BUSINESS decision: instructors have historically tolerated these issues (bud macerates especially).
    confirmed_major_codes: tuple[str, ...] = ("R-WARN-", "R-DOSE-HIGHER", "R-DJR-HIGHER")
    confirmed_major_confidence: float = 0.9

    @property
    def mistral_api_key(self) -> str | None:
        return _read_key("MISTRAL_API_KEY")

    @property
    def db_password(self) -> str:
        return os.environ.get("db_password", "")

    def public_dict(self) -> dict:
        """Settings as written to the run manifest. Contains no secret (the key and password are properties)."""
        d = asdict(self)
        d["data_dir"] = str(self.data_dir)
        d["prompt_versions"] = prompt_versions()
        return d


def prompt_text(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def prompt_hash(name: str) -> str:
    """Short hash of a prompt file. It is part of the cache keys: editing a prompt invalidates only its stage."""
    return hashlib.sha256(prompt_text(name).encode("utf-8")).hexdigest()[:12]


def prompt_versions() -> dict[str, str]:
    return {p.name: prompt_hash(p.name) for p in sorted(PROMPTS_DIR.glob("*.md"))}


def price_of(model: str) -> ModelPrice:
    # Unknown model: assume an expensive one, so the budget guard errs on the safe side.
    return PRICES.get(model, ModelPrice(2.0, 8.0, 0.2, 5.0))
