# pylint: disable=too-many-positional-arguments,too-many-locals
"""
TODO Docstring
"""
from typing import Any, AsyncGenerator, Callable, Generator, Optional, Union

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


class YodaLLM(CustomLLM):
    """
    TODO Docstring
    """

    def __init__(self, *, target_model: str = "openai/gpt-4o-mini", **kwargs: Any) -> None:
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
            altered_messages = messages + [_YODA_SYSTEM_PROMPT]
            optional_params.pop("max_tokens", None)  # TODO Get rid of this line ?

            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-completion")

            if model == "litellm-responses":
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                print(f"RESPONSES RESPONSES {model} RESPONSES RESPONSES")
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                response = litellm.responses(
                    model=self.target_model,
                    input=altered_messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                print(f"COMPLETIONS COMPLETIONS {model} COMPLETIONS COMPLETIONS")
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                response = litellm.completion(
                    model=self.target_model,
                    messages=altered_messages,
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
            altered_messages = messages + [_YODA_SYSTEM_PROMPT]
            optional_params.pop("max_tokens", None)  # TODO Get rid of this line ?

            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-acompletion")

            if model == "litellm-responses":
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                print(f"RESPONSES RESPONSES {model} RESPONSES RESPONSES")
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                response = await litellm.responses(
                    model=self.target_model,
                    input=altered_messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                print(f"COMPLETIONS COMPLETIONS {model} COMPLETIONS COMPLETIONS")
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                response = await litellm.acompletion(
                    model=self.target_model,
                    messages=altered_messages,
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
            altered_messages = messages + [_YODA_SYSTEM_PROMPT]
            optional_params.pop("max_tokens", None)  # TODO Get rid of this line ?
            optional_params["stream"] = True

            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-streaming")

            if model == "litellm-responses":
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                print(f"RESPONSES RESPONSES {model} RESPONSES RESPONSES")
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                response = litellm.responses(
                    model=self.target_model,
                    input=altered_messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                print(f"COMPLETIONS COMPLETIONS {model} COMPLETIONS COMPLETIONS")
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                response = litellm.completion(
                    model=self.target_model,
                    messages=altered_messages,
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
            altered_messages = messages + [_YODA_SYSTEM_PROMPT]
            optional_params.pop("max_tokens", None)  # TODO Get rid of this line ?
            optional_params["stream"] = True

            # For Langfuse
            optional_params.setdefault("metadata", {}).setdefault("trace_name", "OUTBOUND-from-astreaming")

            if model == "litellm-responses":
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                print(f"RESPONSES RESPONSES {model} RESPONSES RESPONSES")
                print("RESPONSES RESPONSES RESPONSES RESPONSES RESPONSES")
                response = await litellm.responses(
                    model=self.target_model,
                    input=altered_messages,
                    logger_fn=logger_fn,
                    headers=headers or {},
                    timeout=timeout,
                    client=client,
                    drop_params=True,  # Drop any params that are not supported by the provider
                    **optional_params,
                )
            else:
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                print(f"COMPLETIONS COMPLETIONS {model} COMPLETIONS COMPLETIONS")
                print("COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS COMPLETIONS")
                response = await litellm.acompletion(
                    model=self.target_model,
                    messages=altered_messages,
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


yoda_llm = YodaLLM()
