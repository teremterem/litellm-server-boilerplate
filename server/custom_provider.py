"""Custom LiteLLM provider that appends a Yoda-speak system prompt and forwards to OpenAI.

Implements completion, acompletion, streaming, astreaming and converts provider tokens
to a generic streaming format for the proxy.
"""
from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, Generator, List

from litellm import acompletion, completion
from litellm.llms.custom_llm import CustomLLM  # type: ignore[attr-defined]

from .streaming_utils import to_generic_streaming_chunk


YODA_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Always respond in Yoda-speak: short, inverted sentences, wise tone. "
        "Rephrase any reply into the manner of speech used by Yoda from Star Wars."
    ),
}


class YodaSpeakLLM(CustomLLM):
    """A custom LLM wrapper that enforces Yoda-speak, then delegates to a base model."""

    provider_name = "yoda-speak"

    def __init__(self, base_model: str | None = None) -> None:
        # Default underlying model can be overridden via config
        self.base_model = base_model or "openai/gpt-5"

    @staticmethod
    def _append_yoda(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Copy to avoid mutating user input
        new_messages = list(messages)
        new_messages.append(YODA_SYSTEM_PROMPT)
        return new_messages

    # Synchronous non-streaming
    def completion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Any:  # type: ignore[override]
        """Forward to underlying model after appending Yoda system prompt."""
        model_to_use = self.base_model or model
        yoda_messages = self._append_yoda(messages)
        # Ensure we are not accidentally streaming here
        kwargs.pop("stream", None)
        return completion(model=model_to_use, messages=yoda_messages, **kwargs)

    # Async non-streaming
    async def acompletion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Any:  # type: ignore[override]
        model_to_use = self.base_model or model
        yoda_messages = self._append_yoda(messages)
        kwargs.pop("stream", None)
        return await acompletion(model=model_to_use, messages=yoda_messages, **kwargs)

    # Synchronous streaming
    def streaming(
        self, model: str, messages: List[Dict[str, Any]], **kwargs: Any
    ) -> Generator[Dict[str, Any], None, None]:  # type: ignore[override]
        model_to_use = self.base_model or model
        yoda_messages = self._append_yoda(messages)
        # Force stream=True for underlying call
        kwargs["stream"] = True
        stream = completion(model=model_to_use, messages=yoda_messages, **kwargs)
        for chunk in stream:
            yield to_generic_streaming_chunk(chunk)

    # Async streaming
    async def astreaming(
        self, model: str, messages: List[Dict[str, Any]], **kwargs: Any
    ) -> AsyncGenerator[Dict[str, Any], None]:  # type: ignore[override]
        model_to_use = self.base_model or model
        yoda_messages = self._append_yoda(messages)
        kwargs["stream"] = True
        astream = await acompletion(model=model_to_use, messages=yoda_messages, **kwargs)
        async for chunk in astream:
            yield to_generic_streaming_chunk(chunk)

