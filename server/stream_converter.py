"""
Utility functions for converting streaming responses to GenericStreamingChunk.
"""

import uuid
from typing import Any, Dict, Union

from litellm.types.utils import GenericStreamingChunk, ModelResponse


def convert_to_generic_streaming_chunk(chunk: Union[ModelResponse, Dict[str, Any]]) -> GenericStreamingChunk:
    """
    Convert various streaming chunk formats to GenericStreamingChunk.

    This function handles streaming responses from different providers supported by LiteLLM.
    and converts them to the standardized GenericStreamingChunk format.

    Args:
        chunk: The streaming chunk from any LiteLLM-supported provider

    Returns:
        GenericStreamingChunk: Standardized streaming chunk
    """
    # If it's already a GenericStreamingChunk, return as-is
    if isinstance(chunk, GenericStreamingChunk):
        return chunk

    # Handle ModelResponse objects (most common case for LiteLLM)
    if hasattr(chunk, "choices") and hasattr(chunk, "model"):
        return _convert_model_response_to_generic_chunk(chunk)

    # Handle dictionary format
    if isinstance(chunk, dict):
        return _convert_dict_to_generic_chunk(chunk)

    # Fallback: create a minimal GenericStreamingChunk
    return GenericStreamingChunk(
        id=str(uuid.uuid4()),
        object="chat.completion.chunk",
        created=0,
        model="unknown",
        choices=[
            {
                "index": 0,
                "delta": {"content": str(chunk) if chunk else ""},
                "finish_reason": None,
            }
        ],
    )


def _convert_model_response_to_generic_chunk(response: ModelResponse) -> GenericStreamingChunk:
    """
    Convert ModelResponse to GenericStreamingChunk.

    Args:
        response: ModelResponse object from LiteLLM

    Returns:
        GenericStreamingChunk: Converted streaming chunk
    """
    # Extract basic properties
    chunk_id = getattr(response, "id", str(uuid.uuid4()))
    model = getattr(response, "model", "unknown")
    created = getattr(response, "created", 0)
    object_type = getattr(response, "object", "chat.completion.chunk")

    # Convert choices
    choices = []
    if hasattr(response, "choices") and response.choices:
        for i, choice in enumerate(response.choices):
            delta = {}
            finish_reason = None

            # Extract delta content
            if hasattr(choice, "delta"):
                delta_obj = choice.delta
                if hasattr(delta_obj, "content") and delta_obj.content is not None:
                    delta["content"] = delta_obj.content
                if hasattr(delta_obj, "role") and delta_obj.role is not None:
                    delta["role"] = delta_obj.role
                if hasattr(delta_obj, "function_call") and delta_obj.function_call is not None:
                    delta["function_call"] = delta_obj.function_call
                if hasattr(delta_obj, "tool_calls") and delta_obj.tool_calls is not None:
                    delta["tool_calls"] = delta_obj.tool_calls

            # Extract finish reason
            if hasattr(choice, "finish_reason"):
                finish_reason = choice.finish_reason

            choices.append(
                {
                    "index": getattr(choice, "index", i),
                    "delta": delta,
                    "finish_reason": finish_reason,
                }
            )
    else:
        # Create empty choice if none exist
        choices.append(
            {
                "index": 0,
                "delta": {},
                "finish_reason": None,
            }
        )

    # Handle usage information if present
    usage = None
    if hasattr(response, "usage") and response.usage:
        usage = {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
            "completion_tokens": getattr(response.usage, "completion_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0),
        }

    # Create GenericStreamingChunk
    generic_chunk = GenericStreamingChunk(
        id=chunk_id,
        object=object_type,
        created=created,
        model=model,
        choices=choices,
    )

    # Add usage if present
    if usage:
        generic_chunk.usage = usage

    return generic_chunk


def _convert_dict_to_generic_chunk(chunk_dict: Dict[str, Any]) -> GenericStreamingChunk:
    """
    Convert dictionary format to GenericStreamingChunk.

    Args:
        chunk_dict: Dictionary representation of streaming chunk

    Returns:
        GenericStreamingChunk: Converted streaming chunk
    """
    # Extract or generate basic properties
    chunk_id = chunk_dict.get("id", str(uuid.uuid4()))
    model = chunk_dict.get("model", "unknown")
    created = chunk_dict.get("created", 0)
    object_type = chunk_dict.get("object", "chat.completion.chunk")

    # Convert choices
    choices = []
    if "choices" in chunk_dict and chunk_dict["choices"]:
        for choice in chunk_dict["choices"]:
            choices.append(
                {
                    "index": choice.get("index", 0),
                    "delta": choice.get("delta", {}),
                    "finish_reason": choice.get("finish_reason"),
                }
            )
    else:
        # Create empty choice if none exist
        choices.append(
            {
                "index": 0,
                "delta": {},
                "finish_reason": None,
            }
        )

    # Create GenericStreamingChunk
    generic_chunk = GenericStreamingChunk(
        id=chunk_id,
        object=object_type,
        created=created,
        model=model,
        choices=choices,
    )

    # Add usage if present
    if "usage" in chunk_dict:
        generic_chunk.usage = chunk_dict["usage"]

    return generic_chunk
