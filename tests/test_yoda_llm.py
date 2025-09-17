from types import SimpleNamespace

import pytest

from server.streaming import convert_stream
from server.yoda_llm import YodaSpeakLLM


def test_system_prompt_appended_once() -> None:
    llm = YodaSpeakLLM()
    payload = {"messages": [{"role": "user", "content": "Hello"}]}

    prepared = llm._prepare_kwargs(payload)  # pylint: disable=protected-access

    assert prepared["messages"][-1]["content"].startswith("Regardless of the request")
    assert len(prepared["messages"]) == 2


@pytest.mark.parametrize(
    "chunk",
    [
        SimpleNamespace(chunk={"choices": [{"delta": {"content": "Hello"}}]}),
        SimpleNamespace(choices=[{"delta": {"content": "Hello"}}]),
    ],
)
def test_convert_stream_handles_basic_chunks(chunk: SimpleNamespace) -> None:
    generic = next(iter(convert_stream([chunk])))
    assert generic.choices[0].delta.content == "Hello"
