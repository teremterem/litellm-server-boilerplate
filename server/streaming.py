"""Utilities for normalizing LiteLLM streaming payloads."""

from __future__ import annotations

from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from typing import Any

from litellm.types.llm_response import (
    GenericDelta,
    GenericStreamingChunk,
    GenericStreamingChoice,
    ModelResponseStream,
)

_TEXTUAL_CONTENT_KEYS = ("text", "content", "completion", "delta")


def convert_stream(
    stream: Iterable[ModelResponseStream],
) -> Iterator[GenericStreamingChunk]:
    """Convert provider specific stream chunks into LiteLLM generic chunks."""

    for chunk in stream:
        yield _ensure_generic_chunk(chunk)


def convert_async_stream(
    stream: AsyncIterable[ModelResponseStream],
) -> AsyncIterator[GenericStreamingChunk]:
    """Async variant of ``convert_stream``."""

    async def _generator() -> AsyncIterator[GenericStreamingChunk]:
        async for chunk in stream:
            yield _ensure_generic_chunk(chunk)

    return _generator()


def _ensure_generic_chunk(chunk: ModelResponseStream) -> GenericStreamingChunk:
    if isinstance(chunk, GenericStreamingChunk):
        return chunk

    to_generic = getattr(chunk, "to_generic_stream_chunk", None)
    if callable(to_generic):
        generic_chunk = to_generic()
        if isinstance(generic_chunk, GenericStreamingChunk):
            return generic_chunk

    payload = getattr(chunk, "chunk", None)
    provider = getattr(chunk, "provider", None)
    usage = getattr(chunk, "usage", None)
    provider_response = getattr(chunk, "provider_response", None)

    if payload is None:
        payload = getattr(chunk, "raw_chunk", None)
    if payload is None and isinstance(chunk, dict):
        payload = chunk

    choices_payload: list[Any] = []
    if isinstance(payload, dict):
        raw_choices = payload.get("choices")
        if isinstance(raw_choices, list):
            choices_payload = raw_choices
    choice_attr = getattr(chunk, "choices", None)
    if isinstance(choice_attr, list) and not choices_payload:
        choices_payload = choice_attr

    if not choices_payload and payload is not None:
        choices_payload = [_wrap_choice_like(payload)]

    choices = _build_generic_choices(choices_payload)

    try:
        return GenericStreamingChunk(
            choices=choices,
            provider_chunk=payload,
            provider_response=provider_response,
            provider=provider,
            usage=usage,
        )
    except Exception:  # pylint: disable=broad-except
        return GenericStreamingChunk(choices=choices)


def _build_generic_choices(payload: Iterable[Any]) -> list[GenericStreamingChoice]:
    generic_choices: list[GenericStreamingChoice] = []
    for index, choice in enumerate(payload):
        if isinstance(choice, GenericStreamingChoice):
            generic_choices.append(choice)
            continue

        finish_reason: str | None = None
        raw_delta: Any = None

        if isinstance(choice, dict):
            finish_reason = choice.get("finish_reason")
            if "delta" in choice:
                raw_delta = choice["delta"]
            elif "message" in choice:
                raw_delta = choice["message"]
            elif "content" in choice:
                raw_delta = {"content": choice["content"]}
            elif "text" in choice:
                raw_delta = {"content": choice["text"]}
            else:
                raw_delta = _pull_text_payload(choice)
            choice_index = choice.get("index", index)
        else:
            choice_index = index
            raw_delta = choice

        delta = _normalize_delta(raw_delta)
        generic_choices.append(
            GenericStreamingChoice(
                index=choice_index,
                finish_reason=finish_reason,
                delta=delta,
            )
        )

    return generic_choices


def _normalize_delta(raw_delta: Any) -> GenericDelta:
    if isinstance(raw_delta, GenericDelta):
        return raw_delta

    role: str | None = None
    content: Any = None
    tool_calls: Any = None

    if isinstance(raw_delta, dict):
        role = raw_delta.get("role")
        tool_calls = raw_delta.get("tool_calls") or raw_delta.get("tools")
        content = _extract_content_from_dict(raw_delta)
    elif raw_delta is not None:
        content = str(raw_delta)

    normalized_content = None
    if isinstance(content, list):
        normalized_content = _combine_content_list(content)
    elif content is not None:
        normalized_content = str(content)

    return GenericDelta(role=role, content=normalized_content, tool_calls=tool_calls)


def _extract_content_from_dict(data: dict[str, Any]) -> Any:
    if "content" in data:
        return data["content"]

    for key in _TEXTUAL_CONTENT_KEYS:
        if key in data:
            return data[key]

    return data


def _combine_content_list(segments: list[Any]) -> str:
    parts: list[str] = []
    for segment in segments:
        if isinstance(segment, dict):
            if "text" in segment:
                parts.append(str(segment["text"]))
            elif "content" in segment:
                parts.append(str(segment["content"]))
        elif segment is not None:
            parts.append(str(segment))
    return "".join(parts)


def _pull_text_payload(data: dict[str, Any]) -> dict[str, Any]:
    fallback: dict[str, Any] = {}
    for key in _TEXTUAL_CONTENT_KEYS:
        if key in data:
            fallback["content"] = data[key]
            break
    if not fallback:
        fallback["content"] = str(data)
    return fallback


def _wrap_choice_like(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"content": payload}
