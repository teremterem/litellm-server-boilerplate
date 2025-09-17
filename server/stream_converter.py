"""Stream conversion utilities for LiteLLM proxy server."""

import json
import time
from typing import AsyncIterator, Iterator, Union

from litellm.types.utils import GenericStreamingChunk, ModelResponse, ModelResponseStream
from litellm.utils import CustomStreamWrapper


def convert_to_generic_chunk(
    chunk: Union[ModelResponse, ModelResponseStream], model: str, created_at: float
) -> GenericStreamingChunk:
    """Convert a ModelResponseStream chunk to a GenericStreamingChunk.

    This function handles conversion from various LiteLLM providers to the standard
    GenericStreamingChunk format expected by the proxy server.

    Args:
        chunk: The response chunk from the model provider
        model: The model name being used
        created_at: Timestamp when the response was created

    Returns:
        GenericStreamingChunk: Standardized chunk format
    """
    # Handle different chunk types from various providers
    if hasattr(chunk, "choices") and chunk.choices:
        # Standard OpenAI-style response
        choice = chunk.choices[0]
        delta = getattr(choice, "delta", {})

        # Extract content from delta
        content = ""
        if hasattr(delta, "content") and delta.content:
            content = delta.content
        elif isinstance(delta, dict) and "content" in delta:
            content = delta.get("content", "")

        # Extract role from delta
        role = None
        if hasattr(delta, "role") and delta.role:
            role = delta.role
        elif isinstance(delta, dict) and "role" in delta:
            role = delta.get("role")

        # Check if this is the end of the stream
        finish_reason = getattr(choice, "finish_reason", None)

        return GenericStreamingChunk(
            text=content,
            is_finished=(finish_reason is not None),
            finish_reason=finish_reason,
            usage=getattr(chunk, "usage", None),
            index=getattr(choice, "index", 0),
            logprobs=getattr(choice, "logprobs", None),
        )

    # Handle cases where chunk doesn't have choices (fallback)
    elif hasattr(chunk, "content"):
        return GenericStreamingChunk(
            text=chunk.content,
            is_finished=getattr(chunk, "is_finished", False),
            finish_reason=getattr(chunk, "finish_reason", None),
            usage=getattr(chunk, "usage", None),
        )

    # Handle dictionary-style responses
    elif isinstance(chunk, dict):
        choices = chunk.get("choices", [])
        if choices:
            choice = choices[0]
            delta = choice.get("delta", {})
            content = delta.get("content", "")
            finish_reason = choice.get("finish_reason")

            return GenericStreamingChunk(
                text=content,
                is_finished=(finish_reason is not None),
                finish_reason=finish_reason,
                usage=chunk.get("usage"),
                index=choice.get("index", 0),
            )

    # Default fallback
    return GenericStreamingChunk(
        text="",
        is_finished=True,
        finish_reason="error",
        usage=None,
    )


def stream_converter(response: Iterator[ModelResponseStream], model: str) -> Iterator[GenericStreamingChunk]:
    """Convert a stream of ModelResponseStream chunks to GenericStreamingChunk.

    Args:
        response: Iterator of ModelResponseStream chunks from the provider
        model: The model name being used

    Yields:
        GenericStreamingChunk: Converted chunks in standard format
    """
    created_at = time.time()

    for chunk in response:
        try:
            converted_chunk = convert_to_generic_chunk(chunk, model, created_at)
            yield converted_chunk
        except Exception as e:
            # Log error and yield error chunk
            print(f"Error converting chunk: {e}")
            yield GenericStreamingChunk(
                text="",
                is_finished=True,
                finish_reason="error",
                usage=None,
            )
            break


async def astream_converter(
    response: AsyncIterator[ModelResponseStream], model: str
) -> AsyncIterator[GenericStreamingChunk]:
    """Async version of stream converter.

    Args:
        response: Async iterator of ModelResponseStream chunks from the provider
        model: The model name being used

    Yields:
        GenericStreamingChunk: Converted chunks in standard format
    """
    created_at = time.time()

    async for chunk in response:
        try:
            converted_chunk = convert_to_generic_chunk(chunk, model, created_at)
            yield converted_chunk
        except Exception as e:
            # Log error and yield error chunk
            print(f"Error converting async chunk: {e}")
            yield GenericStreamingChunk(
                text="",
                is_finished=True,
                finish_reason="error",
                usage=None,
            )
            break
