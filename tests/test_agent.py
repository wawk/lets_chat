from llm.llm_wrapper import LLM
from unittest.mock import MagicMock
from core.agent import Agent 

def test_agent_uses_llm_for_reply():
    # llm = LLM(provider="openai", model="gpt-4o-mini")
    llm = MagicMock()
    llm.invoke.return_value = "Hi there!"
    agent = Agent(llm=llm)

    reply = agent.handle_user_message("Hello")

    assert reply == "Hi there!"
    llm.invoke.assert_called_once_with([{"role": "user", "content": "Hello"}])
    # assert isinstance(reply, str)
    # assert len(reply > 0)

def test_agent_includes_system_prompt():
    llm = MagicMock()
    llm.invoke.return_value = "Hi"

    agent = Agent(
        llm=llm,
        system_prompt="You are a helpful assistant."
    )

    agent.handle_user_message("Hello")

    llm.invoke.assert_called_once_with([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ])

def test_agent_sends_conversation_history():
        llm = MagicMock()
        llm.invoke.side_effect = ["Hi there!", "Hi there!"]

        agent = Agent(llm=llm)
        agent.handle_user_message("Hello")
        agent.handle_user_message("How are you")

        llm.invoke.assert_called_with([
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you"}
        ])

def test_agent_stores_assistant_messages():
     llm = MagicMock()
     llm.invoke.return_value = "Hi there!"

     agent = Agent(llm=llm)

     reply = agent.handle_user_message("Hello")

     # Agent should store the assistant reply
     assert agent.history[-1]["role"] == "assistant"
     assert agent.history[-1]["content"] == "Hi there!"