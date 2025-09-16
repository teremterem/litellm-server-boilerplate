"""
Custom LLM implementation that adds Yoda-speak system prompt to all requests.
"""

from typing import Any, AsyncIterator, Iterator, List, Optional, Union

import litellm
from litellm.llms.custom_llm import CustomLLM
from litellm.types.utils import ModelResponse

from server.streaming_converter import convert_to_generic_streaming_chunk


class YodaLLM(CustomLLM):
    """
    Custom LLM that adds a Yoda-speak system prompt to all requests.
    """

    YODA_SYSTEM_PROMPT = (
        "Always respond in Yoda-speak (the manner of speaking of Yoda from Star Wars). "
        "Use inverted sentence structure, place verbs at the end of sentences, and use "
        "characteristic Yoda phrases like 'hmm', 'yes', and speak with wisdom."
    )

    def completion(
        self,
        messages: List[dict],
        api_base: Optional[str] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[bool] = None,
        logging_obj: Optional[Any] = None,
        custom_llm_provider: Optional[str] = None,
        logger_fn: Optional[Any] = None,
        optional_params: Optional[dict] = None,
        acompletion: Optional[bool] = None,
        stream: Optional[bool] = False,
        **kwargs: Any,
    ) -> Union[ModelResponse, Iterator]:
        """
        Handle synchronous completion requests.
        """
        # Add Yoda system prompt to messages
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5
        if stream:
            return self.streaming(
                messages=modified_messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                logging_obj=logging_obj,
                custom_llm_provider=custom_llm_provider,
                logger_fn=logger_fn,
                optional_params=optional_params,
                **kwargs,
            )

        response = litellm.completion(
            model="openai/gpt-4o",  # Using gpt-4o as gpt-5 doesn't exist yet
            messages=modified_messages,
            stream=False,
            **optional_params if optional_params else {},
        )
        return response

    async def acompletion(
        self,
        messages: List[dict],
        api_base: Optional[str] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[bool] = None,
        logging_obj: Optional[Any] = None,
        custom_llm_provider: Optional[str] = None,
        logger_fn: Optional[Any] = None,
        optional_params: Optional[dict] = None,
        stream: Optional[bool] = False,
        **kwargs: Any,
    ) -> Union[ModelResponse, AsyncIterator]:
        """
        Handle asynchronous completion requests.
        """
        # Add Yoda system prompt to messages
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5
        if stream:
            return self.astreaming(
                messages=modified_messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                logging_obj=logging_obj,
                custom_llm_provider=custom_llm_provider,
                logger_fn=logger_fn,
                optional_params=optional_params,
                **kwargs,
            )

        response = await litellm.acompletion(
            model="openai/gpt-4o",  # Using gpt-4o as gpt-5 doesn't exist yet
            messages=modified_messages,
            stream=False,
            **optional_params if optional_params else {},
        )
        return response

    def streaming(
        self,
        messages: List[dict],
        api_base: Optional[str] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[bool] = None,
        logging_obj: Optional[Any] = None,
        custom_llm_provider: Optional[str] = None,
        logger_fn: Optional[Any] = None,
        optional_params: Optional[dict] = None,
        **kwargs: Any,
    ) -> Iterator:
        """
        Handle synchronous streaming requests.
        """
        # Add Yoda system prompt to messages
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5 with streaming
        stream_response = litellm.completion(
            model="openai/gpt-4o",  # Using gpt-4o as gpt-5 doesn't exist yet
            messages=modified_messages,
            stream=True,
            **optional_params if optional_params else {},
        )

        # Convert ModelResponseStream to GenericStreamingChunk
        for chunk in stream_response:
            yield convert_to_generic_streaming_chunk(chunk)

    async def astreaming(
        self,
        messages: List[dict],
        api_base: Optional[str] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[bool] = None,
        logging_obj: Optional[Any] = None,
        custom_llm_provider: Optional[str] = None,
        logger_fn: Optional[Any] = None,
        optional_params: Optional[dict] = None,
        **kwargs: Any,
    ) -> AsyncIterator:
        """
        Handle asynchronous streaming requests.
        """
        # Add Yoda system prompt to messages
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5 with streaming
        stream_response = await litellm.acompletion(
            model="openai/gpt-4o",  # Using gpt-4o as gpt-5 doesn't exist yet
            messages=modified_messages,
            stream=True,
            **optional_params if optional_params else {},
        )

        # Convert ModelResponseStream to GenericStreamingChunk
        async for chunk in stream_response:
            yield convert_to_generic_streaming_chunk(chunk)

    def _add_yoda_prompt(self, messages: List[dict]) -> List[dict]:
        """
        Add Yoda system prompt to the end of messages.
        """
        modified_messages = messages.copy()
        # Append system prompt at the end
        modified_messages.append({"role": "system", "content": self.YODA_SYSTEM_PROMPT})
        return modified_messages
