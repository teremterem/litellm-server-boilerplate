"""
Stream converter utility to convert ModelResponseStream to GenericStreamingChunk.
Supports multiple LLM providers through LiteLLM.
"""

# pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
# pylint: disable=broad-exception-caught,too-many-nested-blocks

from typing import Any, AsyncIterator, Iterator, Union
from litellm.types.utils import GenericStreamingChunk


def convert_model_stream_to_generic_stream(
    stream: Union[Iterator, AsyncIterator], is_async: bool = False
) -> Union[Iterator[GenericStreamingChunk], AsyncIterator[GenericStreamingChunk]]:
    """
    Convert a stream of ModelResponse chunks to GenericStreamingChunk format.

    This function handles conversion for various LLM providers supported by LiteLLM,
    including OpenAI, Anthropic, Cohere, Hugging Face, and others.

    Args:
        stream: Iterator or AsyncIterator of model response chunks
        is_async: Whether the stream is async

    Returns:
        Iterator or AsyncIterator of GenericStreamingChunk objects
    """
    if is_async:
        return _async_convert_stream(stream)
    return _sync_convert_stream(stream)


def _sync_convert_stream(stream: Iterator) -> Iterator[GenericStreamingChunk]:
    """Synchronous stream conversion."""
    for chunk in stream:
        generic_chunk = _convert_chunk_to_generic(chunk)
        if generic_chunk:
            yield generic_chunk


async def _async_convert_stream(
    stream: AsyncIterator,
) -> AsyncIterator[GenericStreamingChunk]:
    """Asynchronous stream conversion."""
    async for chunk in stream:
        generic_chunk = _convert_chunk_to_generic(chunk)
        if generic_chunk:
            yield generic_chunk


def _convert_openai_style(chunk: Any) -> GenericStreamingChunk:
    """Convert OpenAI-style response chunks."""
    generic_chunk = GenericStreamingChunk()
    if hasattr(chunk, "choices") and chunk.choices:
        choice = chunk.choices[0]
        delta = getattr(choice, "delta", None)

        if delta:
            # Extract content from delta
            if hasattr(delta, "content"):
                generic_chunk.text = delta.content
            elif hasattr(delta, "text"):
                generic_chunk.text = delta.text
            elif isinstance(delta, dict):
                generic_chunk.text = delta.get("content") or delta.get("text", "")

            # Extract function calls if present
            if hasattr(delta, "function_call"):
                generic_chunk.tool_use = delta.function_call
            elif hasattr(delta, "tool_calls"):
                generic_chunk.tool_use = delta.tool_calls

        # Set finish reason if present
        if hasattr(choice, "finish_reason"):
            generic_chunk.finish_reason = choice.finish_reason

        # Preserve usage information if present
        if hasattr(chunk, "usage"):
            generic_chunk.usage = chunk.usage

    return generic_chunk


def _convert_anthropic_style(chunk: Any) -> GenericStreamingChunk:
    """Convert Anthropic-style response chunks."""
    generic_chunk = GenericStreamingChunk()
    if hasattr(chunk, "delta"):
        delta = chunk.delta

        if hasattr(delta, "text"):
            generic_chunk.text = delta.text
        elif hasattr(delta, "content"):
            generic_chunk.text = delta.content
        elif isinstance(delta, dict):
            generic_chunk.text = delta.get("text") or delta.get("content", "")

        if hasattr(chunk, "type") and chunk.type == "message_stop":
            generic_chunk.finish_reason = "stop"

    return generic_chunk


def _convert_dict_response(chunk: dict) -> GenericStreamingChunk:
    """Convert dictionary-based response chunks."""
    generic_chunk = GenericStreamingChunk()

    # Try various common patterns in dict responses
    if "choices" in chunk and chunk["choices"]:
        choice = chunk["choices"][0]
        if "delta" in choice:
            delta = choice["delta"]
            generic_chunk.text = delta.get("content") or delta.get("text", "")
        if "finish_reason" in choice:
            generic_chunk.finish_reason = choice["finish_reason"]

    elif "text" in chunk:
        generic_chunk.text = chunk["text"]

    elif "content" in chunk:
        generic_chunk.text = chunk["content"]

    elif "delta" in chunk:
        delta = chunk["delta"]
        if isinstance(delta, dict):
            generic_chunk.text = delta.get("text") or delta.get("content", "")
        else:
            generic_chunk.text = str(delta)

    return generic_chunk


def _convert_chunk_to_generic(chunk: Any) -> GenericStreamingChunk:
    """
    Convert a single chunk from various provider formats to GenericStreamingChunk.

    Handles different response formats from various providers:
    - OpenAI/Azure OpenAI: ChatCompletionChunk with choices[].delta
    - Anthropic: MessageStreamEvent with delta.text
    - Cohere: StreamedChatResponse with text
    - Google/Vertex AI: GenerateContentResponse with text
    - Others: Generic ModelResponse format
    """
    try:
        # If it's already a GenericStreamingChunk, return as is
        if isinstance(chunk, GenericStreamingChunk):
            return chunk

        # Handle OpenAI-style responses
        if hasattr(chunk, "choices"):
            return _convert_openai_style(chunk)

        # Handle Anthropic-style responses
        if hasattr(chunk, "delta"):
            return _convert_anthropic_style(chunk)

        # Handle Cohere-style responses
        if hasattr(chunk, "text"):
            generic_chunk = GenericStreamingChunk()
            generic_chunk.text = chunk.text
            if hasattr(chunk, "is_finished") and chunk.is_finished:
                generic_chunk.finish_reason = "stop"
            return generic_chunk

        # Handle Google/Vertex AI style responses
        if hasattr(chunk, "candidates"):
            generic_chunk = GenericStreamingChunk()
            if chunk.candidates:
                candidate = chunk.candidates[0]
                if hasattr(candidate, "content"):
                    content = candidate.content
                    if hasattr(content, "parts"):
                        for part in content.parts:
                            if hasattr(part, "text"):
                                generic_chunk.text = part.text
                                break
                if hasattr(candidate, "finish_reason"):
                    generic_chunk.finish_reason = candidate.finish_reason
            return generic_chunk

        # Handle dict-based responses
        if isinstance(chunk, dict):
            return _convert_dict_response(chunk)

        # Handle string responses (raw text)
        if isinstance(chunk, str):
            generic_chunk = GenericStreamingChunk()
            generic_chunk.text = chunk
            return generic_chunk

        # If we can't convert, try to create a generic chunk with string representation
        generic_chunk = GenericStreamingChunk()
        generic_chunk.text = str(chunk) if chunk else ""
        return generic_chunk

    except Exception as e:
        # In case of any conversion error, return an empty chunk rather than failing
        print(f"Warning: Failed to convert chunk: {e}")
        generic_chunk = GenericStreamingChunk()
        generic_chunk.text = ""
        return generic_chunk
