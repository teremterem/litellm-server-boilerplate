"""
Custom LLM implementation that adds Yoda-speak system prompt to all requests.
"""

# pylint: disable=too-many-arguments,too-many-locals,unused-argument

from typing import Any, Dict, Optional, Union
import litellm
from litellm.llms.custom_llm import CustomLLM
from litellm.types.utils import ModelResponse


class YodaSpeakModel(CustomLLM):
    """Custom LLM that forwards requests to OpenAI GPT-5 with Yoda-speak system prompt."""

    YODA_SYSTEM_PROMPT = (
        "You must respond in the manner of speaking of Yoda from Star Wars. "
        "Use Yoda's characteristic inverted sentence structure where the "
        "object-subject-verb order is used. For example, instead of 'I am ready', "
        "say 'Ready, I am'. Instead of 'You must learn', say 'Learn, you must'. "
        "Keep your wisdom and insight, but express everything in Yoda's unique "
        "speaking pattern."
    )

    def __init__(self):
        super().__init__()
        self.target_model = "openai/gpt-5"

    def _append_yoda_prompt(self, messages: list) -> list:
        """Append Yoda system prompt to the messages."""
        messages_copy = messages.copy()
        messages_copy.append({"role": "system", "content": self.YODA_SYSTEM_PROMPT})
        return messages_copy

    def completion(
        self,
        model: str,
        messages: list,
        api_base: Optional[str] = None,
        custom_prompt_dict: Optional[Dict] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[callable] = None,
        encoding: Optional[Any] = None,
        api_key: Optional[str] = None,
        logging_obj: Optional[Any] = None,
        optional_params: Optional[Dict] = None,
        litellm_params: Optional[Dict] = None,
        logger_fn: Optional[callable] = None,
        **kwargs,
    ) -> Union[ModelResponse, str]:
        """Synchronous completion with Yoda-speak prompt."""
        if custom_prompt_dict is None:
            custom_prompt_dict = {}
        if model_response is None:
            model_response = ModelResponse()

        modified_messages = self._append_yoda_prompt(messages)

        response = litellm.completion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key,
            **(optional_params if optional_params else {}),
        )

        return response

    async def acompletion(
        self,
        model: str,
        messages: list,
        api_base: Optional[str] = None,
        custom_prompt_dict: Optional[Dict] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[callable] = None,
        encoding: Optional[Any] = None,
        api_key: Optional[str] = None,
        logging_obj: Optional[Any] = None,
        optional_params: Optional[Dict] = None,
        litellm_params: Optional[Dict] = None,
        logger_fn: Optional[callable] = None,
        **kwargs,
    ) -> Union[ModelResponse, str]:
        """Asynchronous completion with Yoda-speak prompt."""
        if custom_prompt_dict is None:
            custom_prompt_dict = {}
        if model_response is None:
            model_response = ModelResponse()

        modified_messages = self._append_yoda_prompt(messages)

        response = await litellm.acompletion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key,
            **(optional_params if optional_params else {}),
        )

        return response

    def streaming(
        self,
        model: str,
        messages: list,
        api_base: Optional[str] = None,
        custom_prompt_dict: Optional[Dict] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[callable] = None,
        encoding: Optional[Any] = None,
        api_key: Optional[str] = None,
        logging_obj: Optional[Any] = None,
        optional_params: Optional[Dict] = None,
        litellm_params: Optional[Dict] = None,
        logger_fn: Optional[callable] = None,
        **kwargs,
    ):
        """Synchronous streaming with Yoda-speak prompt."""
        if custom_prompt_dict is None:
            custom_prompt_dict = {}
        if model_response is None:
            model_response = ModelResponse()

        modified_messages = self._append_yoda_prompt(messages)

        if optional_params is None:
            optional_params = {}
        optional_params["stream"] = True

        response = litellm.completion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key,
            **optional_params,
        )

        # Import stream converter here to avoid circular imports
        # pylint: disable=import-outside-toplevel
        from .stream_converter import convert_model_stream_to_generic_stream

        return convert_model_stream_to_generic_stream(response)

    async def astreaming(
        self,
        model: str,
        messages: list,
        api_base: Optional[str] = None,
        custom_prompt_dict: Optional[Dict] = None,
        model_response: Optional[ModelResponse] = None,
        print_verbose: Optional[callable] = None,
        encoding: Optional[Any] = None,
        api_key: Optional[str] = None,
        logging_obj: Optional[Any] = None,
        optional_params: Optional[Dict] = None,
        litellm_params: Optional[Dict] = None,
        logger_fn: Optional[callable] = None,
        **kwargs,
    ):
        """Asynchronous streaming with Yoda-speak prompt."""
        if custom_prompt_dict is None:
            custom_prompt_dict = {}
        if model_response is None:
            model_response = ModelResponse()

        modified_messages = self._append_yoda_prompt(messages)

        if optional_params is None:
            optional_params = {}
        optional_params["stream"] = True

        response = await litellm.acompletion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key,
            **optional_params,
        )

        # Import stream converter here to avoid circular imports
        # pylint: disable=import-outside-toplevel
        from .stream_converter import (
            convert_model_stream_to_generic_stream,
        )

        async for chunk in convert_model_stream_to_generic_stream(response, is_async=True):
            yield chunk
