from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, Optional

try:
    # LiteLLM >=1.44 introduced GenericStreamingChunk
    from litellm.types.utils import GenericStreamingChunk
except Exception:  # pragma: no cover - fallback for older versions
    GenericStreamingChunk = Dict[str, Any]  # type: ignore


def _safe_get(dct: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = dct
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def model_stream_to_generic_chunks(
    token_stream: Iterator[Dict[str, Any]] | AsyncIterator[Dict[str, Any]],
) -> Iterator[GenericStreamingChunk] | AsyncIterator[GenericStreamingChunk]:
    """
    Convert provider-specific ModelResponseStream tokens to GenericStreamingChunk.

    This is a best-effort converter intended to work across providers supported by LiteLLM.
    It handles common shapes from OpenAI, Anthropic, Azure OpenAI, Mistral, Groq, etc.

    - Expects input items to be dict-like (LiteLLM typically yields dicts for stream chunks)
    - Yields a structure with at least: {"choices": [{"delta": {"content": str}, "index": int}], "model": str}
    - When provider supplies tool/function calls or system deltas, we emit them in a generic way when present.
    """

    async def _agen() -> AsyncIterator[GenericStreamingChunk]:
        async for chunk in token_stream:  # type: ignore[operator]
            yield _convert_single_chunk(chunk)

    def _gen() -> Iterator[GenericStreamingChunk]:
        for chunk in token_stream:  # type: ignore[operator]
            yield _convert_single_chunk(chunk)

    if hasattr(token_stream, "__anext__"):
        return _agen()
    return _gen()


def _convert_single_chunk(chunk: Dict[str, Any]) -> GenericStreamingChunk:
    # Common top-level hints
    model = chunk.get("model") or _safe_get(chunk, "provider", default="unknown-model")

    # OpenAI-style delta
    delta_content: Optional[str] = _safe_get(chunk, "choices", 0, "delta", "content")

    # Anthropic-style content delta
    if delta_content is None:
        delta_content = _safe_get(chunk, "delta", "text")

    # Mistral-style
    if delta_content is None:
        delta_content = _safe_get(chunk, "data", "choices", 0, "delta", "content")

    # Groq/OpenAI compatible
    if delta_content is None:
        delta_content = _safe_get(chunk, "data", "delta")

    # Fallback to any string-like
    if delta_content is None and isinstance(chunk.get("content"), str):
        delta_content = chunk["content"]

    # Tool/function call deltas (best-effort generic shape)
    tool_calls = _safe_get(chunk, "choices", 0, "delta", "tool_calls")
    function_call = _safe_get(chunk, "choices", 0, "delta", "function_call")

    generic_choice: Dict[str, Any] = {
        "index": _safe_get(chunk, "choices", 0, "index", default=0) or 0,
        "delta": {},
    }

    if delta_content is not None:
        generic_choice["delta"]["content"] = delta_content

    if tool_calls is not None:
        generic_choice["delta"]["tool_calls"] = tool_calls

    if function_call is not None:
        generic_choice["delta"]["function_call"] = function_call

    generic_chunk: Dict[str, Any] = {
        "model": model,
        "choices": [generic_choice],
    }

    # Include finish_reason if available
    finish_reason = _safe_get(chunk, "choices", 0, "finish_reason")
    if finish_reason:
        generic_chunk["choices"][0]["finish_reason"] = finish_reason

    # Include usage counters if present
    usage = chunk.get("usage")
    if usage:
        generic_chunk["usage"] = usage

    return generic_chunk  # type: ignore[return-value]
