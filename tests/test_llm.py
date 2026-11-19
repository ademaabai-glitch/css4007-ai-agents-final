"""Tests use a clearly labelled FAKE model, so no API key is needed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm import ask


class FakeReply:
    def __init__(self, content):
        self.content = content


class FakeLLM:
    """FAKE model for tests, not a real LLM."""
    def invoke(self, messages):
        return FakeReply("fake answer")


class BrokenLLM:
    """FAKE model that always fails, to test error handling."""
    def invoke(self, messages):
        raise ConnectionError("no network")


def test_ask_returns_model_text():
    assert ask(FakeLLM(), "bouquet") == "fake answer"


def test_empty_input_does_not_call_model():
    assert "Please write" in ask(BrokenLLM(), "   ")


def test_model_failure_gives_message_not_crash():
    assert "failed" in ask(BrokenLLM(), "bouquet")


def test_make_llm_without_key_gives_clear_error(monkeypatch):
    import pytest
    from llm import make_llm
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        make_llm()


def test_ask_sends_system_prompt_and_trimmed_text():
    from llm import SYSTEM_PROMPT

    class RecordingLLM:
        """FAKE model that remembers what it was sent."""
        def invoke(self, messages):
            self.messages = messages
            return FakeReply("ok")

    llm = RecordingLLM()
    ask(llm, "  bouquet  ")
    assert llm.messages[0] == ("system", SYSTEM_PROMPT)
    assert llm.messages[1] == ("human", "bouquet")
