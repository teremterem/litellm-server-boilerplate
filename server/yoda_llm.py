"""Yoda LLM implementation that forwards requests to OpenAI with Yoda-style prompts."""

import os
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional

import litellm
from litellm.llms.custom_llm import CustomLLM
from litellm.types.utils import GenericStreamingChunk, ModelResponse

from .stream_converter import astream_converter, stream_converter


class YodaLLM(CustomLLM):
    """Custom LLM that forwards requests to OpenAI GPT-5 with Yoda-style system prompts."""

    def __init__(self):
        super().__init__()
        self.model_name = "yoda-gpt-5"
        self.target_model = "openai/gpt-5"
        self.yoda_system_prompt = {
            "role": "system",
            "content": (
                "Always respond in the manner of speaking of Yoda from Star Wars you must. "
                "Rearrange your words in Yoda's distinctive syntax, you should. "
                "Wise and cryptic, but helpful, your responses must be. "
                "Use 'hmm' and other Yoda-like expressions, appropriate they are."
            ),
        }

    def _add_yoda_prompt(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add Yoda system prompt to the messages list."""
        # Check if there's already a system message at the beginning
        modified_messages = messages.copy()

        # Find the last system message or add at the beginning
        system_indices = [i for i, msg in enumerate(modified_messages) if msg.get("role") == "system"]

        if system_indices:
            # Insert after the last system message
            last_system_index = system_indices[-1]
            modified_messages.insert(last_system_index + 1, self.yoda_system_prompt)
        else:
            # Add at the beginning if no system messages exist
            modified_messages.insert(0, self.yoda_system_prompt)

        return modified_messages

    def completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        api_type: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse:
        """Complete a chat request with Yoda-style prompting."""
        # Add Yoda system prompt
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5
        response = litellm.completion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            **kwargs,
        )

        return response

    async def acompletion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        api_type: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse:
        """Async completion with Yoda-style prompting."""
        # Add Yoda system prompt
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5
        response = await litellm.acompletion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            **kwargs,
        )

        return response

    def streaming(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        api_type: Optional[str] = None,
        **kwargs: Any,
    ) -> Iterator[GenericStreamingChunk]:
        """Stream completion with Yoda-style prompting."""
        # Add Yoda system prompt
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5 with streaming
        response = litellm.completion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            stream=True,
            **kwargs,
        )

        # Convert the stream to GenericStreamingChunk format
        return stream_converter(response, model)

    async def astreaming(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        api_base: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        api_type: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncIterator[GenericStreamingChunk]:
        """Async stream completion with Yoda-style prompting."""
        # Add Yoda system prompt
        modified_messages = self._add_yoda_prompt(messages)

        # Forward to OpenAI GPT-5 with async streaming
        response = await litellm.acompletion(
            model=self.target_model,
            messages=modified_messages,
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            stream=True,
            **kwargs,
        )

        # Convert the async stream to GenericStreamingChunk format
        async for chunk in astream_converter(response, model):
            yield chunk
