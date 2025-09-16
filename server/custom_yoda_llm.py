from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, List

from litellm import completion, acompletion, stream as litellm_stream, astream as litellm_astream
from litellm.llms.custom_llm import CustomLLM

from .streaming_utils import model_stream_to_generic_chunks


YODA_SYSTEM_SUFFIX = {
    "role": "system",
    "content": (
        "Answer you must in Yoda-speak. Use inverted grammar and wise tone. "
        "Short and cryptic, your style should be, hmmm."
    ),
}


class YodaLLM(CustomLLM):
    """Custom LLM appending a Yoda system prompt, then forwarding to target provider."""

    def _append_yoda(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        new_messages = list(messages)
        new_messages.append(YODA_SYSTEM_SUFFIX)
        return new_messages

    # Non-streaming
    def completion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
        forward_model = kwargs.pop("forward_model", "openai/gpt-5")
        final_messages = self._append_yoda(messages)
        return completion(model=forward_model, messages=final_messages, **kwargs)

    async def acompletion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Dict[str, Any]:
        forward_model = kwargs.pop("forward_model", "openai/gpt-5")
        final_messages = self._append_yoda(messages)
        return await acompletion(model=forward_model, messages=final_messages, **kwargs)

    # Streaming
    def streaming(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Iterator[Dict[str, Any]]:
        forward_model = kwargs.pop("forward_model", "openai/gpt-5")
        final_messages = self._append_yoda(messages)
        underlying_stream = litellm_stream(model=forward_model, messages=final_messages, **kwargs)
        return model_stream_to_generic_chunks(underlying_stream)  # type: ignore[return-value]

    async def astreaming(
        self, model: str, messages: List[Dict[str, Any]], **kwargs: Any
    ) -> AsyncIterator[Dict[str, Any]]:
        forward_model = kwargs.pop("forward_model", "openai/gpt-5")
        final_messages = self._append_yoda(messages)
        underlying_stream = litellm_astream(model=forward_model, messages=final_messages, **kwargs)
        async for generic in model_stream_to_generic_chunks(underlying_stream):  # type: ignore[arg-type]
            yield generic


__all__ = ["YodaLLM"]
