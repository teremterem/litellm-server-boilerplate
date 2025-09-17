from typing import Any, AsyncIterator, Dict, Iterator, List
from litellm import CustomLLM, completion, acompletion, stream, astream
from .stream_convert import to_generic_stream_chunk, map_stream


class YodaLLM(CustomLLM):
    yoda_system = {
        "role": "system",
        "content": "Always answer in Yoda-speak: inverted syntax, wise, concise.",
    }

    def _with_yoda(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        msgs = list(messages or [])
        msgs.append(self.yoda_system)
        return msgs

    def completion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Any:
        return completion(model="openai/gpt-5", messages=self._with_yoda(messages), **kwargs)

    async def acompletion(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Any:
        return await acompletion(model="openai/gpt-5", messages=self._with_yoda(messages), **kwargs)

    def streaming(self, model: str, messages: List[Dict[str, Any]], **kwargs: Any) -> Iterator[Dict[str, Any]]:
        gen = stream(model="openai/gpt-5", messages=self._with_yoda(messages), **kwargs)
        return map_stream(gen)

    async def astreaming(
        self, model: str, messages: List[Dict[str, Any]], **kwargs: Any
    ) -> AsyncIterator[Dict[str, Any]]:
        agen = astream(model="openai/gpt-5", messages=self._with_yoda(messages), **kwargs)
        async for ch in agen:
            yield to_generic_stream_chunk(ch)


yoda_llm = YodaLLM()
