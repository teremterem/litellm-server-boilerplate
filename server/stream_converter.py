"""
Utilities to convert provider-specific streaming tokens to a GenericStreamingChunk shape.
"""

from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator, Dict, Iterator, Optional


def _extract_text_from_chunk(chunk: Dict[str, Any]) -> Optional[str]:
    """
    Best-effort extraction of textual delta from various provider chunk shapes.
    """
    if not isinstance(chunk, dict):
        return None
    choices = chunk.get("choices")
    if isinstance(choices, list) and choices:
        delta = choices[0].get("delta") if isinstance(choices[0], dict) else None
        if isinstance(delta, dict):
            text = delta.get("content") or delta.get("text")
            if isinstance(text, str):
                return text
        text = choices[0].get("text")
        if isinstance(text, str):
            return text
    data = chunk.get("data")
    if isinstance(data, dict):
        text = data.get("content") or data.get("text")
        if isinstance(text, str):
            return text
    for key in ("content", "text"):
        val = chunk.get(key)
        if isinstance(val, str):
            return val
    return None


def _make_generic_chunk(text: str, model: Optional[str] = None) -> Dict[str, Any]:
    """
    Create an OpenAI-style chat.completion.chunk with a text delta.
    """
    return {
        "id": None,
        "object": "chat.completion.chunk",
        "model": model or "",
        "choices": [
            {
                "index": 0,
                "delta": {"content": text},
                "finish_reason": None,
            }
        ],
    }


def convert_stream(upstream: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """
    Convert a sync iterator of provider chunks into GenericStreamingChunk items.
    """
    for raw in upstream:
        text = _extract_text_from_chunk(raw)
        if text:
            yield _make_generic_chunk(text, model=raw.get("model"))
    yield {
        "id": None,
        "object": "chat.completion.chunk",
        "model": "",
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop",
            }
        ],
    }


async def aconvert_stream(upstream: Any) -> AsyncIterator[Dict[str, Any]]:
    """
    Convert an async iterator (or plain iterator) of provider chunks to generic chunks.
    """
    if hasattr(upstream, "__aiter__"):
        async for raw in upstream:  # type: ignore
            text = _extract_text_from_chunk(raw)
            if text:
                yield _make_generic_chunk(text, model=raw.get("model"))
    else:
        loop = asyncio.get_running_loop()
        it = iter(upstream)
        while True:
            try:
                raw = await loop.run_in_executor(None, next, it)
            except StopIteration:
                break
            text = _extract_text_from_chunk(raw)
            if text:
                yield _make_generic_chunk(text, model=raw.get("model"))
    yield {
        "id": None,
        "object": "chat.completion.chunk",
        "model": "",
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop",
            }
        ],
    }
