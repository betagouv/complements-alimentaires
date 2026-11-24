"""Asynchronous LLM client (Mistral), designed to be swappable.

- async, with a token-bucket rate limiter and a concurrency semaphore (instead of a global sleep);
- retries with exponential back-off + jitter on 429 / 5xx / timeouts, honouring Retry-After;
- strict structured outputs (JSON schema derived from Pydantic), with one repair pass;
- content-addressed cache for every deterministic call;
- token, estimated cost and latency tracking per stage, plus a budget guard.

To switch provider, implement the same interface (chat_json, chat_tools, ocr, ocr_image, embed):
the rest of the pipeline does not depend on Mistral.
"""

from __future__ import annotations

import asyncio
import contextvars
import copy
import json
import random
import time
from dataclasses import dataclass, field
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from ..cache import Cache
from ..config import Settings, price_of

API = "https://api.mistral.ai/v1"

# Key of the declaration being analysed, so that each call's cost is attributed to its declaration
# (declarations run concurrently; a ContextVar follows each asyncio task).
CURRENT_KEY: contextvars.ContextVar[str | None] = contextvars.ContextVar("decl_key", default=None)


class BudgetExceeded(RuntimeError):
    """Raised before any call once the run's estimated spend reaches Settings.budget_usd."""


class LLMError(RuntimeError):
    """Non-retryable API error, or retries exhausted."""


@dataclass
class Usage:
    """Ledger of every model call of a run (cost, tokens, latency, cache hits)."""

    budget_usd: float
    calls: list[dict] = field(default_factory=list)

    @property
    def cost(self) -> float:
        return sum(c["cost_usd"] for c in self.calls)

    def record(self, **call) -> None:
        call.setdefault("decl", CURRENT_KEY.get())
        self.calls.append(call)

    def cost_for(self, key: str) -> float:
        return sum(c["cost_usd"] for c in self.calls if c.get("decl") == key)

    def check(self) -> None:
        if self.cost >= self.budget_usd:
            raise BudgetExceeded(f"Budget reached: {self.cost:.2f} $ >= {self.budget_usd:.2f} $")

    def summary(self) -> dict:
        by_stage: dict[str, dict] = {}
        for c in self.calls:
            s = by_stage.setdefault(
                c["stage"], {"calls": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0, "pages": 0}
            )
            s["calls"] += 1
            s["cost_usd"] += c["cost_usd"]
            s["input_tokens"] += c.get("input_tokens", 0)
            s["output_tokens"] += c.get("output_tokens", 0)
            s["pages"] += c.get("pages", 0)
        return {"total_cost_usd": round(self.cost, 4), "calls": len(self.calls), "by_stage": by_stage}


class RateLimiter:
    """Token-bucket limiter: at most `rate` requests per second on average."""

    def __init__(self, rate: float):
        self.rate = rate
        self._next = 0.0
        self._lock = asyncio.Lock()

    async def wait(self) -> None:
        # Each caller books the next free slot under the lock, then sleeps outside it.
        async with self._lock:
            now = time.monotonic()
            delay = self._next - now
            self._next = max(now, self._next) + 1.0 / self.rate
        if delay > 0:
            await asyncio.sleep(delay)


def strict_schema(model: type[BaseModel]) -> dict:
    """'Strict' JSON schema for Mistral structured outputs: $refs inlined, every field required,
    no additional properties. Field descriptions are kept: they are part of the prompt."""
    raw = model.model_json_schema()
    defs = raw.pop("$defs", {})

    def resolve(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node:
                name = node["$ref"].split("/")[-1]
                return resolve(copy.deepcopy(defs[name]))
            out = {k: resolve(v) for k, v in node.items() if k not in ("title", "default")}
            if out.get("type") == "object" and "properties" in out:
                out["additionalProperties"] = False
                out["required"] = list(out["properties"].keys())
            return out
        if isinstance(node, list):
            return [resolve(x) for x in node]
        return node

    return resolve(raw)


def _content_text(message: dict) -> str:
    content = message.get("content")
    if isinstance(content, list):  # "reasoning" models return thinking + text blocks
        return "".join(part.get("text", "") for part in content if part.get("type") == "text")
    return content or ""


class LLMClient:
    def __init__(self, settings: Settings, cache: Cache, usage: Usage):
        key = settings.mistral_api_key
        if not key:
            raise LLMError("MISTRAL_API_KEY not found (environment variable or ai_v2.env file).")
        self.settings = settings
        self.cache = cache
        self.usage = usage
        self._http = httpx.AsyncClient(
            base_url=API,
            headers={"Authorization": f"Bearer {key}"},
            timeout=httpx.Timeout(settings.request_timeout_s, connect=20),
            limits=httpx.Limits(max_connections=settings.max_concurrent_llm_calls * 2),
        )
        self._sem = asyncio.Semaphore(settings.max_concurrent_llm_calls)
        self._limiter = RateLimiter(settings.requests_per_second)

    async def aclose(self) -> None:
        await self._http.aclose()

    # ------------------------------------------------------------------ transport
    async def _post(self, path: str, payload: dict) -> tuple[dict, float]:
        """POST with rate limiting, bounded concurrency and retries. Returns (json, latency in s)."""
        self.usage.check()
        delay = 2.0
        last_error: Exception | None = None
        for attempt in range(self.settings.max_retries + 1):
            await self._limiter.wait()
            async with self._sem:
                start = time.monotonic()
                try:
                    resp = await self._http.post(path, json=payload)
                except (httpx.TimeoutException, httpx.TransportError) as e:
                    last_error = e
                    resp = None
                latency = time.monotonic() - start
            if resp is not None and resp.status_code == 200:
                return resp.json(), latency
            # Client errors (400, 401, 422...) will not get better by retrying.
            if resp is not None and resp.status_code not in (408, 409, 429, 500, 502, 503, 504):
                raise LLMError(f"{path} HTTP {resp.status_code}: {resp.text[:500]}")
            if resp is not None:
                last_error = LLMError(f"{path} HTTP {resp.status_code}: {resp.text[:200]}")
                retry_after = resp.headers.get("retry-after")
                if retry_after:
                    try:
                        delay = max(delay, float(retry_after))
                    except ValueError:
                        pass
            await asyncio.sleep(delay + random.uniform(0, delay / 2))
            delay = min(delay * 2, 60)
        raise LLMError(f"{path}: failed after {self.settings.max_retries} retries ({last_error})")

    def _record_chat(self, stage: str, model: str, data: dict, latency: float) -> dict:
        """Record the cost of a chat call. Cached prompt tokens are billed at the cached price."""
        u = data.get("usage") or {}
        prompt = u.get("prompt_tokens", 0)
        cached = (u.get("prompt_tokens_details") or {}).get("cached_tokens", 0) or 0
        completion = u.get("completion_tokens", 0)
        p = price_of(model)
        cost = ((prompt - cached) * p.input_per_m + cached * p.cached_input_per_m + completion * p.output_per_m) / 1e6
        rec = {
            "stage": stage,
            "model": model,
            "input_tokens": prompt,
            "cached_tokens": cached,
            "output_tokens": completion,
            "cost_usd": cost,
            "latency_s": round(latency, 2),
        }
        self.usage.record(**rec)
        return rec

    # ------------------------------------------------------------------ chat JSON
    async def chat_json(
        self,
        stage: str,
        model: str,
        messages: list[dict],
        output: type[BaseModel],
        *,
        temperature: float = 0.0,
        max_tokens: int = 8000,
        cache_parts: dict | None = None,
    ) -> BaseModel:
        """Call with a strict structured output, validated by Pydantic.

        Cached when `cache_parts` is given: the key combines the stage, the model, the output schema
        and `cache_parts` (callers put the prompt hash and the input in it).
        """
        key = None
        if cache_parts is not None:
            key = self.cache.key(
                stage, model=model, out=output.__name__, json_schema=strict_schema(output), parts=cache_parts
            )
            hit = self.cache.get(key)
            if hit is not None:
                self.usage.record(stage=stage, model=model, cost_usd=0.0, cached_hit=True, latency_s=0)
                return output.model_validate(hit)

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": output.__name__, "schema": strict_schema(output), "strict": True},
            },
        }
        result = None
        for attempt in range(2):
            data, latency = await self._post("/chat/completions", payload)
            self._record_chat(stage, model, data, latency)
            choice = data["choices"][0]
            text = _content_text(choice["message"])
            try:
                result = output.model_validate(json.loads(text))
                break
            except (json.JSONDecodeError, ValidationError) as e:
                if attempt == 1:
                    raise LLMError(f"{stage}: invalid output after the repair pass ({e})") from e
                # Repair pass: send the validation error back to the model (prompt text, in French).
                payload = copy.deepcopy(payload)
                payload["messages"] = messages + [
                    {"role": "assistant", "content": text[:20000]},
                    {
                        "role": "user",
                        "content": f"La réponse ne respecte pas le schéma ({str(e)[:800]}). "
                        "Renvoie uniquement le JSON corrigé, complet.",
                    },
                ]
        if key is not None:
            self.cache.set(key, result.model_dump(mode="json"))
        return result

    # ------------------------------------------------------------------ chat + tools (agent)
    async def chat_tools(
        self,
        stage: str,
        model: str,
        messages: list[dict],
        tools: list[dict],
        *,
        temperature: float = 0.0,
        max_tokens: int = 4000,
        tool_choice: str = "auto",
    ) -> dict:
        """One function-calling turn. Not cached: the agent loop depends on previous tool results."""
        payload = {
            "model": model,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "parallel_tool_calls": True,
        }
        data, latency = await self._post("/chat/completions", payload)
        self._record_chat(stage, model, data, latency)
        return data["choices"][0]["message"]

    # ------------------------------------------------------------------ OCR
    async def ocr(self, url: str, is_pdf: bool, file_sha256: str, max_pages: int) -> dict:
        """OCR of a whole file, by URL. Cached by file content (sha256), not by URL."""
        model = self.settings.model_ocr
        key = self.cache.key("ocr", model=model, file=file_sha256, max_pages=max_pages)
        hit = self.cache.get(key)
        if hit is not None:
            self.usage.record(stage="ocr", model=model, cost_usd=0.0, cached_hit=True, latency_s=0)
            return hit
        document = {"type": "document_url", "document_url": url} if is_pdf else {"type": "image_url", "image_url": url}
        # No image annotation and no base64 images back: we only need the text (cheaper, faster).
        payload = {"model": model, "document": document, "include_image_base64": False}
        if is_pdf:
            payload["pages"] = list(range(max_pages))
        try:
            data, latency = await self._post("/ocr", payload)
        except LLMError as e:
            # The API rejects page indexes beyond the end of a short PDF: retry without the page list.
            if is_pdf and "pages" in str(e).lower():
                payload.pop("pages")
                data, latency = await self._post("/ocr", payload)
            else:
                raise
        pages_n = (data.get("usage_info") or {}).get("pages_processed", len(data.get("pages", [])))
        cost = pages_n * price_of(model).per_1000_pages / 1000
        self.usage.record(stage="ocr", model=model, pages=pages_n, cost_usd=cost, latency_s=round(latency, 2))
        result = {
            "pages": [
                {"index": p.get("index", i), "markdown": p.get("markdown", ""), "dimensions": p.get("dimensions")}
                for i, p in enumerate(data.get("pages", []))
            ],
            "model": data.get("model", model),
        }
        self.cache.set(key, result)
        return result

    async def ocr_image(self, data_url: str, cache_id: str) -> str:
        """OCR of one image given as a data URL (a rendered page, possibly rotated or a tile), cached.

        `cache_id` identifies the image deterministically (file sha256 + page + rotation/tile), which
        avoids hashing the base64 payload.
        """
        model = self.settings.model_ocr
        key = self.cache.key("ocr_image", model=model, id=cache_id)
        hit = self.cache.get(key)
        if hit is not None:
            self.usage.record(stage="ocr", model=model, cost_usd=0.0, cached_hit=True, latency_s=0)
            return hit
        data, latency = await self._post(
            "/ocr",
            {"model": model, "document": {"type": "image_url", "image_url": data_url}, "include_image_base64": False},
        )
        cost = price_of(model).per_1000_pages / 1000
        self.usage.record(stage="ocr", model=model, pages=1, cost_usd=cost, latency_s=round(latency, 2))
        text = "\n".join(p.get("markdown", "") for p in data.get("pages", []))
        self.cache.set(key, text)
        return text

    # ------------------------------------------------------------------ embeddings
    async def embed(self, texts: list[str], stage: str = "embed") -> list[list[float]]:
        """Embeddings, cached per text. Only cache misses are sent, in batches of 64."""
        model = self.settings.model_embed
        out: list[list[float] | None] = [None] * len(texts)
        todo: list[tuple[int, str, str]] = []
        for i, t in enumerate(texts):
            key = self.cache.key("embed", model=model, text=t)
            hit = self.cache.get(key)
            if hit is not None:
                out[i] = hit
            else:
                todo.append((i, t, key))

        async def run_batch(batch):
            data, latency = await self._post("/embeddings", {"model": model, "input": [t for _, t, _ in batch]})
            u = data.get("usage") or {}
            cost = u.get("prompt_tokens", 0) * price_of(model).input_per_m / 1e6
            self.usage.record(
                stage=stage, model=model, input_tokens=u.get("prompt_tokens", 0), cost_usd=cost, latency_s=latency
            )
            for (i, _, key), item in zip(batch, data["data"]):
                out[i] = item["embedding"]
                self.cache.set(key, item["embedding"])

        batches = [todo[i : i + 64] for i in range(0, len(todo), 64)]
        await asyncio.gather(*(run_batch(b) for b in batches))
        return out  # type: ignore[return-value]
