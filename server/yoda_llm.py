"""
Custom LiteLLM implementation that adds Yoda-speak system prompt to all requests.
"""

from typing import Any, Dict, Iterator, List, Optional

from litellm import completion, acompletion
from litellm.llms.custom_llm import CustomLLM
from litellm.types.utils import GenericStreamingChunk, ModelResponse

from .stream_converter import convert_to_generic_streaming_chunk


class YodaLLM(CustomLLM):
    """
    Custom LiteLLM that forwards all requests to OpenAI GPT-5 with Yoda-speak system prompt.
    """

    YODA_SYSTEM_PROMPT = (
        "Always respond in the manner of Yoda from Star Wars. Use his distinctive speech pattern, "
        "wisdom, and grammatical structure. Begin sentences with the predicate, use inverted "
        "word order, and speak with his characteristic cadence and philosophy."
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize YodaLLM instance.
        """
        super().__init__(*args, **kwargs)
        self.model_name = "openai/gpt-5"

    def _add_yoda_prompt(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add Yoda system prompt to the messages.

        Args:
            messages: Original list of messages

        Returns:
            Modified list of messages with Yoda system prompt appended
        """
        modified_messages = messages.copy()
        modified_messages.append({"role": "system", "content": self.YODA_SYSTEM_PROMPT})
        return modified_messages

    def completion(  # pylint: disable=too-many-arguments,too-many-positional-arguments,arguments-differ
        self,
        model: str,
        messages: List[Dict[str, Any]],
        model_response: ModelResponse,
        print_verbose: bool = False,
        encoding=None,
        logging_obj=None,
        optional_params: Optional[Dict[str, Any]] = None,
        litellm_params: Optional[Dict[str, Any]] = None,
        logger_fn=None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> ModelResponse:
        """
        Synchronous completion with Yoda-speak system prompt.
        """
        modified_messages = self._add_yoda_prompt(messages)

        return completion(model=self.model_name, messages=modified_messages, **(optional_params or {}), **kwargs)

    async def acompletion(  # pylint: disable=too-many-arguments,too-many-positional-arguments,arguments-differ
        self,
        model: str,
        messages: List[Dict[str, Any]],
        model_response: ModelResponse,
        print_verbose: bool = False,
        encoding=None,
        logging_obj=None,
        optional_params: Optional[Dict[str, Any]] = None,
        litellm_params: Optional[Dict[str, Any]] = None,
        logger_fn=None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> ModelResponse:
        """
        Asynchronous completion with Yoda-speak system prompt.
        """
        modified_messages = self._add_yoda_prompt(messages)

        return await acompletion(
            model=self.model_name, messages=modified_messages, **(optional_params or {}), **kwargs
        )

    def streaming(  # pylint: disable=too-many-arguments,too-many-positional-arguments,arguments-differ
        self,
        model: str,
        messages: List[Dict[str, Any]],
        model_response: ModelResponse,
        print_verbose: bool = False,
        encoding=None,
        logging_obj=None,
        optional_params: Optional[Dict[str, Any]] = None,
        litellm_params: Optional[Dict[str, Any]] = None,
        logger_fn=None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Iterator[GenericStreamingChunk]:
        """
        Synchronous streaming completion with Yoda-speak system prompt.
        """
        modified_messages = self._add_yoda_prompt(messages)

        stream = completion(
            model=self.model_name, messages=modified_messages, stream=True, **(optional_params or {}), **kwargs
        )

        for chunk in stream:
            yield convert_to_generic_streaming_chunk(chunk)

    async def astreaming(  # pylint: disable=too-many-arguments,too-many-positional-arguments,arguments-differ
        self,
        model: str,
        messages: List[Dict[str, Any]],
        model_response: ModelResponse,
        print_verbose: bool = False,
        encoding=None,
        logging_obj=None,
        optional_params: Optional[Dict[str, Any]] = None,
        litellm_params: Optional[Dict[str, Any]] = None,
        logger_fn=None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Iterator[GenericStreamingChunk]:
        """
        Asynchronous streaming completion with Yoda-speak system prompt.
        """
        modified_messages = self._add_yoda_prompt(messages)

        stream = await acompletion(
            model=self.model_name, messages=modified_messages, stream=True, **(optional_params or {}), **kwargs
        )

        async for chunk in stream:
            yield convert_to_generic_streaming_chunk(chunk)
