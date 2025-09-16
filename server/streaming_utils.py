"""Utilities for converting provider-specific streaming tokens to LiteLLM's generic format.

We aim to convert arbitrary provider streaming chunks (e.g., OpenAI, Anthropic, etc.)
into a shape compatible with LiteLLM's GenericStreamingChunk. We avoid depending on
internal/private types and instead return dicts with the expected structure.

This is a best-effort conversion that should work across many providers. If a field
is missing, we keep sensible fallbacks so the proxy can still relay partial chunks.
"""
from __future__ import annotations

from typing import Any, Dict


def _extract_text_from_openai_like(chunk: Dict[str, Any]) -> str | None:
    """Extract text content from an OpenAI-style chunk.

    Looks for `choices[0].delta.content` or `choices[0].text`.
    """
    try:
        choices = chunk.get("choices") or []
        if not choices:
            return None
        delta = choices[0].get("delta") or {}
        if "content" in delta and delta["content"] is not None:
            return delta["content"]
        if "text" in choices[0] and choices[0]["text"] is not None:
            return choices[0]["text"]
    except Exception:  # pragma: no cover - defensive
        return None
    return None


def _extract_text_from_anthropic_like(chunk: Dict[str, Any]) -> str | None:
    """Extract text from an Anthropic-style event structure.

    Tries paths seen in Claude streaming events: `delta.text` or `completion`.
    """
    try:
        if isinstance(chunk.get("delta"), dict):
            text = chunk["delta"].get("text")
            if text:
                return text
        if "completion" in chunk and chunk["completion"]:
            return chunk["completion"]
    except Exception:  # pragma: no cover - defensive
        return None
    return None


def _extract_text_generic(chunk: Dict[str, Any]) -> str | None:
    """Attempt generic text extraction from various plausible keys."""
    for key in ("content", "text", "delta", "token"):
        if isinstance(chunk.get(key), str):
            return chunk[key]
        if isinstance(chunk.get(key), dict) and isinstance(chunk[key].get("content"), str):
            return chunk[key]["content"]
    return None


def to_generic_streaming_chunk(chunk: Any) -> Dict[str, Any]:
    """Convert any model-specific streaming chunk into a GenericStreamingChunk-like dict.

    The returned dict mirrors OpenAI chat-completions streaming shape that LiteLLM
    commonly accepts when proxying: {"id", "object", "created", "model", "choices": [{"delta": {"content": str}, ...}]}.
    Unknown fields are passed through under top-level keys when helpful.
    """
    # If the chunk is already in the expected dict shape, pass through quickly
    if isinstance(chunk, dict) and "choices" in chunk:
        # Ensure we still normalize to have `delta.content` if possible
        text = _extract_text_from_openai_like(chunk)
        if text is not None:
            first = chunk["choices"][0]
            delta = first.get("delta") or {}
            delta["content"] = text
            first["delta"] = delta
        return chunk

    # Attempt to coerce to dict
    if not isinstance(chunk, dict):
        try:
            chunk = dict(chunk)  # type: ignore[arg-type]
        except Exception:
            chunk = {"raw": chunk}

    model = chunk.get("model")
    created = chunk.get("created")
    chunk_id = chunk.get("id")

    # Try provider-specific heuristics, then fall back to generic
    text = (
        _extract_text_from_openai_like(chunk)
        or _extract_text_from_anthropic_like(chunk)
        or _extract_text_generic(chunk)
        or ""
    )

    # Assemble a GenericStreamingChunk-ish dict
    generic: Dict[str, Any] = {
        "id": chunk_id or "stream-chunk",
        "object": chunk.get("object") or "chat.completion.chunk",
        "created": created or 0,
        "model": model or chunk.get("provider") or "unknown",
        "choices": [
            {
                "index": 0,
                "delta": {"content": text},
                "finish_reason": chunk.get("finish_reason"),
            }
        ],
    }

    return generic

