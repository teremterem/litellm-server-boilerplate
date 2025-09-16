"""
Utility for converting streaming tokens from various providers to GenericStreamingChunk.
"""

from typing import Any

from litellm.types.utils import GenericStreamingChunk, ModelResponseStream


def convert_to_generic_streaming_chunk(chunk: Any) -> GenericStreamingChunk:
    """
    Convert a streaming chunk from any provider to GenericStreamingChunk format.

    This function handles conversion from various provider formats that LiteLLM supports,
    including OpenAI, Anthropic, Google, Azure, Cohere, Replicate, and others.

    Args:
        chunk: The streaming chunk from a provider

    Returns:
        GenericStreamingChunk: Converted chunk in generic format
    """
    # If it's already a GenericStreamingChunk, return as-is
    if isinstance(chunk, GenericStreamingChunk):
        return chunk

    # Handle ModelResponseStream (most common case from LiteLLM)
    if isinstance(chunk, ModelResponseStream):
        return _convert_model_response_stream(chunk)

    # Handle dictionary responses (some providers return raw dicts)
    if isinstance(chunk, dict):
        return _convert_dict_chunk(chunk)

    # Handle other potential formats
    # This is extensible for future provider formats
    return _create_generic_chunk_from_unknown(chunk)


def _convert_model_response_stream(stream: ModelResponseStream) -> GenericStreamingChunk:
    """
    Convert ModelResponseStream to GenericStreamingChunk.
    """
    # Extract content from the first choice if available
    content = None
    finish_reason = None
    tool_calls = None

    if stream.choices and len(stream.choices) > 0:
        choice = stream.choices[0]

        # Extract delta content
        if hasattr(choice, "delta") and choice.delta:
            delta = choice.delta
            if hasattr(delta, "content"):
                content = delta.content
            if hasattr(delta, "tool_calls"):
                tool_calls = delta.tool_calls

        # Extract finish reason
        if hasattr(choice, "finish_reason"):
            finish_reason = choice.finish_reason

    # Create GenericStreamingChunk
    generic_chunk = GenericStreamingChunk(
        id=stream.id if hasattr(stream, "id") else None,
        object=stream.object if hasattr(stream, "object") else "chat.completion.chunk",
        created=stream.created if hasattr(stream, "created") else None,
        model=stream.model if hasattr(stream, "model") else None,
        provider=stream.provider if hasattr(stream, "provider") else None,
        choices=[
            {
                "index": 0,
                "delta": {
                    "content": content,
                    "tool_calls": tool_calls,
                },
                "finish_reason": finish_reason,
            }
        ],
    )

    # Copy over usage information if available
    if hasattr(stream, "usage") and stream.usage:
        generic_chunk.usage = stream.usage

    # Copy over system fingerprint if available
    if hasattr(stream, "system_fingerprint"):
        generic_chunk.system_fingerprint = stream.system_fingerprint

    return generic_chunk


def _convert_dict_chunk(chunk_dict: dict) -> GenericStreamingChunk:
    """
    Convert a dictionary chunk to GenericStreamingChunk.

    This handles raw dictionary responses from various providers.
    """
    # Extract common fields
    chunk_id = chunk_dict.get("id")
    chunk_object = chunk_dict.get("object", "chat.completion.chunk")
    created = chunk_dict.get("created")
    model = chunk_dict.get("model")

    # Handle choices - different providers structure this differently
    choices = []
    if "choices" in chunk_dict:
        for idx, choice in enumerate(chunk_dict["choices"]):
            choice_data = {"index": idx, "delta": {}, "finish_reason": None}

            # Handle delta/message content
            if "delta" in choice:
                delta = choice["delta"]
                if "content" in delta:
                    choice_data["delta"]["content"] = delta["content"]
                if "tool_calls" in delta:
                    choice_data["delta"]["tool_calls"] = delta["tool_calls"]
                if "role" in delta:
                    choice_data["delta"]["role"] = delta["role"]
            elif "message" in choice:
                # Some providers use 'message' instead of 'delta'
                message = choice["message"]
                if "content" in message:
                    choice_data["delta"]["content"] = message["content"]

            # Handle text field (some providers like Cohere)
            if "text" in choice:
                choice_data["delta"]["content"] = choice["text"]

            # Handle finish reason
            if "finish_reason" in choice:
                choice_data["finish_reason"] = choice["finish_reason"]
            elif "stop_reason" in choice:
                # Some providers use 'stop_reason'
                choice_data["finish_reason"] = choice["stop_reason"]

            choices.append(choice_data)

    # Handle providers that don't use 'choices' structure
    if not choices:
        # Anthropic style
        if "content" in chunk_dict:
            choices = [{"index": 0, "delta": {"content": chunk_dict["content"]}, "finish_reason": None}]
        # Cohere style
        elif "text" in chunk_dict:
            choices = [{"index": 0, "delta": {"content": chunk_dict["text"]}, "finish_reason": None}]
        # Google/Vertex AI style
        elif "candidates" in chunk_dict:
            for idx, candidate in enumerate(chunk_dict["candidates"]):
                content = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
                choices.append({"index": idx, "delta": {"content": content}, "finish_reason": None})

    # Create GenericStreamingChunk
    generic_chunk = GenericStreamingChunk(
        id=chunk_id,
        object=chunk_object,
        created=created,
        model=model,
        provider=chunk_dict.get("provider"),
        choices=choices if choices else [{"index": 0, "delta": {}, "finish_reason": None}],
    )

    # Add usage if present
    if "usage" in chunk_dict:
        generic_chunk.usage = chunk_dict["usage"]

    # Add system fingerprint if present
    if "system_fingerprint" in chunk_dict:
        generic_chunk.system_fingerprint = chunk_dict["system_fingerprint"]

    return generic_chunk


def _create_generic_chunk_from_unknown(chunk: Any) -> GenericStreamingChunk:
    """
    Create a GenericStreamingChunk from an unknown format.

    This is a fallback for handling unexpected formats.
    """
    # Try to extract any text content
    content = None
    if hasattr(chunk, "text"):
        content = chunk.text
    elif hasattr(chunk, "content"):
        content = chunk.content
    else:
        # Last resort - convert to string
        content = str(chunk) if chunk else None

    return GenericStreamingChunk(
        id=None,
        object="chat.completion.chunk",
        created=None,
        model=None,
        provider=None,
        choices=[{"index": 0, "delta": {"content": content}, "finish_reason": None}],
    )
