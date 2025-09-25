# pylint: disable=too-many-positional-arguments,too-many-locals
from typing import AsyncGenerator, Callable, Generator, Optional, Union

import httpx
import litellm
from litellm import CustomLLM, GenericStreamingChunk, HTTPHandler, ModelResponse, AsyncHTTPHandler

from server.utils import ServerError, to_generic_streaming_chunk


_YODA_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Regardless of the request, respond in Yoda-speak."
        " Short sentences, inverted syntax, and the wisdom of the Jedi, you must use."
    ),
}


class YodaLiteLLMCompletions(CustomLLM):
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
        try:
            # For Langfuse
            optional_params.setdefault("metadata", {})["trace_name"] = "OUTBOUND-from-completion"

            response = litellm.completion(
                model=model,
                messages=messages + [_YODA_SYSTEM_PROMPT],
                logger_fn=logger_fn,
                headers=headers or {},
                timeout=timeout,
                client=client,
                drop_params=True,  # Drop any params that are not supported by the provider
                **optional_params,
            )
            return response

        except Exception as e:
            raise ServerError(e) from e

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
        try:
            # For Langfuse
            optional_params.setdefault("metadata", {})["trace_name"] = "OUTBOUND-from-acompletion"

            response = await litellm.acompletion(
                model=model,
                messages=messages + [_YODA_SYSTEM_PROMPT],
                logger_fn=logger_fn,
                headers=headers or {},
                timeout=timeout,
                client=client,
                drop_params=True,  # Drop any params that are not supported by the provider
                **optional_params,
            )
            return response

        except Exception as e:
            raise ServerError(e) from e

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
        try:
            optional_params["stream"] = True

            # For Langfuse
            optional_params.setdefault("metadata", {})["trace_name"] = "OUTBOUND-from-streaming"

            response = litellm.completion(
                model=model,
                messages=messages + [_YODA_SYSTEM_PROMPT],
                logger_fn=logger_fn,
                headers=headers or {},
                timeout=timeout,
                client=client,
                drop_params=True,  # Drop any params that are not supported by the provider
                **optional_params,
            )
            for chunk in response:
                generic_chunk = to_generic_streaming_chunk(chunk)
                yield generic_chunk

        except Exception as e:
            raise ServerError(e) from e

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
        try:
            optional_params["stream"] = True

            # For Langfuse
            optional_params.setdefault("metadata", {})["trace_name"] = "OUTBOUND-from-astreaming"

            response = await litellm.acompletion(
                model=model,
                messages=messages + [_YODA_SYSTEM_PROMPT],
                logger_fn=logger_fn,
                headers=headers or {},
                timeout=timeout,
                client=client,
                drop_params=True,  # Drop any params that are not supported by the provider
                **optional_params,
            )
            async for chunk in response:
                generic_chunk = to_generic_streaming_chunk(chunk)
                yield generic_chunk

        except Exception as e:
            raise ServerError(e) from e


yoda_litellm_completions = YodaLiteLLMCompletions()
