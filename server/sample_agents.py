# pylint: disable=too-many-positional-arguments,too-many-locals
"""
TODO Docstring
"""
from typing import Any, AsyncGenerator, Callable, Generator, Optional, Union

import httpx
import litellm
from litellm import CustomLLM, GenericStreamingChunk, HTTPHandler, ModelResponse, AsyncHTTPHandler

from server.utils import (
    ServerError,
    convert_chat_messages_to_responses_items,
    convert_chat_params_to_responses,
    convert_responses_to_model_response,
    to_generic_streaming_chunk,
)


_YODA_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Regardless of the request, respond in Yoda-speak."
        " Short sentences, inverted syntax, and the wisdom of the Jedi, you must use."
    ),
}


class YodaLLM(CustomLLM):
    """
    TODO Docstring
    """

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
        try:
            messages = messages + [_YODA_SYSTEM_PROMPT]

            optional_params["stream"] = False
            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-completion")

            if model == "litellm-responses":
                print("\033[1m\033[32mLiteLLM Responses API Request\033[0m")
                response = litellm.responses(  # TODO Check all params are supported
                    model=self.target_model,
                    input=convert_chat_messages_to_responses_items(messages),
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    **convert_chat_params_to_responses(optional_params),
                )
                response = convert_responses_to_model_response(response)
            elif model == "litellm-completions":
                print("\033[1m\033[32mLiteLLM ChatCompletions API Request\033[0m")
                response = litellm.completion(
                    model=self.target_model,
                    messages=messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                raise ValueError(f"Invalid model: {model}")

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
            messages = messages + [_YODA_SYSTEM_PROMPT]

            optional_params["stream"] = False
            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-acompletion")

            if model == "litellm-responses":
                print("\033[1m\033[32mLiteLLM Responses API Request\033[0m")
                response = await litellm.aresponses(  # TODO Check all params are supported
                    model=self.target_model,
                    input=convert_chat_messages_to_responses_items(messages),
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    **convert_chat_params_to_responses(optional_params),
                )
                response = convert_responses_to_model_response(response)
            elif model == "litellm-completions":
                print("\033[1m\033[32mLiteLLM ChatCompletions API Request\033[0m")
                response = await litellm.acompletion(
                    model=self.target_model,
                    messages=messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                raise ValueError(f"Invalid model: {model}")

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
            messages = messages + [_YODA_SYSTEM_PROMPT]

            optional_params["stream"] = True
            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-streaming")

            if model == "litellm-responses":
                print("\033[1m\033[32mLiteLLM Responses API Request\033[0m")
                response = litellm.responses(  # TODO Check all params are supported
                    model=self.target_model,
                    input=convert_chat_messages_to_responses_items(messages),
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    **convert_chat_params_to_responses(optional_params),
                )
            elif model == "litellm-completions":
                print("\033[1m\033[32mLiteLLM ChatCompletions API Request\033[0m")
                response = litellm.completion(
                    model=self.target_model,
                    messages=messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                raise ValueError(f"Invalid model: {model}")

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
            messages = messages + [_YODA_SYSTEM_PROMPT]

            optional_params["stream"] = True
            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-astreaming")

            if model == "litellm-responses":
                print("\033[1m\033[32mLiteLLM Responses API Request\033[0m")
                response = await litellm.aresponses(  # TODO Check all params are supported
                    model=self.target_model,
                    input=convert_chat_messages_to_responses_items(messages),
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    **convert_chat_params_to_responses(optional_params),
                )
            elif model == "litellm-completions":
                print("\033[1m\033[32mLiteLLM ChatCompletions API Request\033[0m")
                response = await litellm.acompletion(
                    model=self.target_model,
                    messages=messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                raise ValueError(f"Invalid model: {model}")

            async for chunk in response:
                generic_chunk = to_generic_streaming_chunk(chunk)
                yield generic_chunk

        except Exception as e:
            raise ServerError(e) from e


yoda_llm = YodaLLM()
