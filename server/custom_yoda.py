"""
Custom LiteLLM provider that appends a Yoda-speak system prompt and forwards to openai/gpt-5.
"""

from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, List

try:
    from litellm.integrations.custom_llm import CustomLLM
except ImportError:
    try:
        from litellm.integrations.custom import CustomLLM
    except ImportError:
        from litellm import CustomLLM

from litellm import acompletion, completion

from server.stream_converter import aconvert_stream, convert_stream


YODA_SYSTEM = {
    "role": "system",
    "content": "Always answer in Yoda-speak. Inverted syntax, wise tone, concise you must be.",
}


def _with_yoda(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Return a new message list with a Yoda-speak system message appended.
    """
    new_messages = list(messages or [])
    new_messages.append(YODA_SYSTEM)
    return new_messages


class CustomYodaLLM(CustomLLM):
    """
    Forwards requests to openai/gpt-5 with an appended Yoda-speak system prompt.
    """

    provider = "custom_yoda"

    def completion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Any:
        """
        Synchronous non-streaming completion with Yoda-speak system prompt.
        """
        _ = model
        target_model = "openai/gpt-5"
        msgs = _with_yoda(messages)
        return completion(model=target_model, messages=msgs, **kwargs)

    async def acompletion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Any:
        """
        Asynchronous non-streaming completion with Yoda-speak system prompt.
        """
        _ = model
        target_model = "openai/gpt-5"
        msgs = _with_yoda(messages)
        return await acompletion(model=target_model, messages=msgs, **kwargs)

    def streaming(
        self, model: str, messages: List[Dict[str, Any]], **kwargs: Any
    ) -> Iterator[Dict[str, Any]]:
        """
        Synchronous streaming completion converted to GenericStreamingChunk format.
        """
        _ = model
        target_model = "openai/gpt-5"
        msgs = _with_yoda(messages)
        kwargs = {**kwargs, "stream": True}
        upstream = completion(model=target_model, messages=msgs, **kwargs)
        return convert_stream(upstream)

    async def astreaming(
        self, model: str, messages: List[Dict[str, Any]], **kwargs: Any
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Asynchronous streaming completion converted to GenericStreamingChunk format.
        """
        _ = model
        target_model = "openai/gpt-5"
        msgs = _with_yoda(messages)
        kwargs = {**kwargs, "stream": True}
        upstream = await acompletion(model=target_model, messages=msgs, **kwargs)
        async for chunk in aconvert_stream(upstream):
            yield chunk
