import pytest
from unittest.mock import patch
from llm.llm_wrapper import LLM


def test_llm_initialization():
    llm = LLM(provider="openai", model="gpt-4o-mini")
    assert llm.provider == "openai"
    assert llm.model == "gpt-4o-mini"


def test_llm_invoke_openai():
    llm = LLM(provider="openai", model="gpt-4o-mini")
    messages = [{"role": "user", "content": "Hello"}]

    # Patch the exact path used inside llm_wrapper.py
    with patch("llm.llm_wrapper.openai") as mock_openai:
        mock_openai.chat.completions.create.return_value = type("obj", (), {
            "choices": [
                type("obj", (), {"message": {"content": "Hi there!"}})
            ]
        })

        response = llm.invoke(messages)

    assert response == "Hi there!"
    mock_openai.chat.completions.create.assert_called_once()


def test_llm_supported_provider():
    llm = LLM(provider="unknown", model="whatever")
    with pytest.raises(ValueError):
        llm.invoke([{"role": "user", "content": "Hello"}])


def test_llm_invalid_messages():
    llm = LLM(provider="openai", model="gpt-4o-mini")
    with pytest.raises(TypeError):
        llm.invoke("not a list")


def test_llm_empty_messages():
    llm = LLM(provider="openai", model="gpt-4o-mini")
    with pytest.raises(ValueError):
        llm.invoke([])
