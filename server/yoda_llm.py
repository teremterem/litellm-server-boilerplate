from typing import Any, AsyncGenerator, Callable, Generator, Optional, Union

import httpx
import litellm
from litellm import CustomLLM, GenericStreamingChunk, HTTPHandler, ModelResponse, AsyncHTTPHandler

from server.streaming import _ensure_generic_chunk


_YODA_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Regardless of the request, respond in Yoda-speak."
        " Short sentences, inverted syntax, and the wisdom of the Jedi, you must use."
    ),
}


class YodaSpeakLLM(CustomLLM):
    """Proxy wrapper that forces Yoda-speak responses from the underlying LLM."""

    def __init__(self, *, target_model: str = "openai/gpt-4o", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.target_model = target_model

    def completion(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable,
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        litellm_params=None,
        logger_fn=None,
        headers=None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        client: Optional[HTTPHandler] = None,
    ) -> ModelResponse:
        optional_params.pop("max_tokens", None)

        response = litellm.completion(
            model=self.target_model,
            messages=messages + [_YODA_SYSTEM_PROMPT],
            logger_fn=logger_fn,
            headers=headers or {},
            timeout=timeout,
            client=client,
            drop_params=True,  # Drop any params that are not supported by the provider
            **optional_params,
        )
        return response

    async def acompletion(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable,
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        litellm_params=None,
        logger_fn=None,
        headers=None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        client: Optional[AsyncHTTPHandler] = None,
    ) -> ModelResponse:
        optional_params.pop("max_tokens", None)

        response = await litellm.acompletion(
            model=self.target_model,
            messages=messages + [_YODA_SYSTEM_PROMPT],
            logger_fn=logger_fn,
            headers=headers or {},
            timeout=timeout,
            client=client,
            drop_params=True,  # Drop any params that are not supported by the provider
            **optional_params,
        )
        return response

    def streaming(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable,
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        litellm_params=None,
        logger_fn=None,
        headers=None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        client: Optional[HTTPHandler] = None,
    ) -> Generator[GenericStreamingChunk, None, None]:
        optional_params["stream"] = True
        optional_params.pop("max_tokens", None)

        response = litellm.completion(
            model=self.target_model,
            messages=messages + [_YODA_SYSTEM_PROMPT],
            logger_fn=logger_fn,
            headers=headers or {},
            timeout=timeout,
            client=client,
            drop_params=True,  # Drop any params that are not supported by the provider
            **optional_params,
        )
        for chunk in response:
            generic_chunk = _ensure_generic_chunk(chunk)
            yield generic_chunk

    async def astreaming(
        self,
        model: str,
        messages: list,
        api_base: str,
        custom_prompt_dict: dict,
        model_response: ModelResponse,
        print_verbose: Callable,
        encoding,
        api_key,
        logging_obj,
        optional_params: dict,
        acompletion=None,
        litellm_params=None,
        logger_fn=None,
        headers=None,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        client: Optional[AsyncHTTPHandler] = None,
    ) -> AsyncGenerator[GenericStreamingChunk, None]:
        optional_params["stream"] = True
        optional_params.pop("max_tokens", None)

        response = await litellm.acompletion(
            model=self.target_model,
            messages=messages + [_YODA_SYSTEM_PROMPT],
            logger_fn=logger_fn,
            headers=headers or {},
            timeout=timeout,
            client=client,
            drop_params=True,  # Drop any params that are not supported by the provider
            **optional_params,
        )
        async for chunk in response:
            generic_chunk = _ensure_generic_chunk(chunk)
            yield generic_chunk


yoda_speak_llm = YodaSpeakLLM()
