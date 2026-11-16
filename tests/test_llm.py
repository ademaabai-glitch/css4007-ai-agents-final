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
