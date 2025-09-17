from typing import Any, Dict, Iterator, Optional


def _extract_text(chunk: Dict[str, Any]) -> Optional[str]:
    if not chunk:
        return None
    if "choices" in chunk:
        choices = chunk.get("choices") or []
        if choices:
            choice = choices[0] or {}
            delta = choice.get("delta") or {}
            if isinstance(delta, dict) and "content" in delta:
                return delta.get("content")
            if "text" in choice:
                return choice.get("text")
            if "content" in choice:
                c = choice.get("content")
                if isinstance(c, str):
                    return c
                if isinstance(c, list):
                    parts = []
                    for p in c:
                        if isinstance(p, dict) and p.get("type") == "text":
                            t = p.get("text")
                            if isinstance(t, dict):
                                parts.append(t.get("value", ""))
                            elif isinstance(t, str):
                                parts.append(t)
                    return "".join(parts) if parts else None
    for key in ("delta", "data", "message", "chunk"):
        val = chunk.get(key)
        if isinstance(val, dict):
            t = val.get("content") or val.get("text")
            if isinstance(t, str):
                return t
    t = chunk.get("content") or chunk.get("text")
    if isinstance(t, str):
        return t
    return None


def _extract_finish_reason(chunk: Dict[str, Any]) -> Optional[str]:
    if "choices" in chunk:
        choices = chunk.get("choices") or []
        if choices:
            choice = choices[0] or {}
            if isinstance(choice, dict):
                fr = choice.get("finish_reason")
                if isinstance(fr, str) or fr is None:
                    return fr
    return chunk.get("finish_reason")


def to_generic_stream_chunk(chunk: Dict[str, Any]) -> Dict[str, Any]:
    text = _extract_text(chunk) or ""
    finish_reason = _extract_finish_reason(chunk)
    return {
        "id": chunk.get("id") or "chunk",
        "object": "chat.completion.chunk",
        "created": chunk.get("created") or 0,
        "model": chunk.get("model") or "",
        "choices": [
            {
                "index": 0,
                "delta": {"content": text} if text else {},
                "finish_reason": finish_reason,
            }
        ],
    }


def map_stream(chunks: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    for ch in chunks:
        yield to_generic_stream_chunk(ch)
