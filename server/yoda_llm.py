"""Custom LiteLLM provider that rewrites prompts for Yoda-speak."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from litellm import acompletion, astream, completion, stream
from litellm.integrations.custom_llm import CustomLLM
from litellm.types.llm_response import GenericStreamingChunk

from .streaming import convert_async_stream, convert_stream

_YODA_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Regardless of the request, respond in Yoda-speak."
        " Short sentences, inverted syntax, and the wisdom of the Jedi, you must use."
    ),
}


class YodaSpeakLLM(CustomLLM):
    """Proxy wrapper that forces Yoda-speak responses from the underlying LLM."""

    def __init__(self, *, target_model: str = "openai/gpt-5", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.target_model = target_model

    def completion(self, *args: Any, **kwargs: Any) -> Any:
        prepared = self._prepare_kwargs(kwargs)
        return completion(*args, **prepared)

    async def acompletion(self, *args: Any, **kwargs: Any) -> Any:
        prepared = self._prepare_kwargs(kwargs)
        return await acompletion(*args, **prepared)

    def streaming(self, *args: Any, **kwargs: Any) -> Iterator[GenericStreamingChunk]:
        prepared = self._prepare_kwargs(kwargs)
        provider_stream = stream(*args, **prepared)
        return convert_stream(provider_stream)

    async def astreaming(self, *args: Any, **kwargs: Any) -> AsyncIterator[GenericStreamingChunk]:
        prepared = self._prepare_kwargs(kwargs)
        provider_stream = astream(*args, **prepared)
        return convert_async_stream(provider_stream)

    def _prepare_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        prepared = dict(kwargs)
        messages = list(prepared.get("messages", []) or [])
        messages.append(_YODA_SYSTEM_PROMPT)
        prepared["messages"] = messages
        prepared.setdefault("model", self.target_model)
        return prepared
