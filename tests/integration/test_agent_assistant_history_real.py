import os
from dotenv import load_dotenv
load_dotenv()

from llm.llm_wrapper import LLM
from agents.agent import Agent
system_prompt = "You are a helpful friendly assistant."
def test_agent_stores_assistant_messages_real():
    # Endure API Key is present
    assert "OPENAI_API_KEY" in os.environ
    llm = LLM(provider = "openai", model = "gpt-4o-mini")
    agent = Agent(llm=llm, system_prompt = system_prompt)

    # First turn
    reply1 = agent.handle_user_message("Hello!")
    assert isinstance(reply1, str)
    assert len(reply1) > 0

    #Second turn
    reply2 = agent.handle_user_message("How are you today?")
    assert isinstance(reply2, str)
    assert len(reply2) > 0

    # History should contain:
    # system -> user -> assistant -> user -> assistant
    assert agent.history[0]["role"] == "system"
    assert agent.history[1]["role"] == "user"
    assert agent.history[2]["role"] == "assistant"
    assert agent.history[3]["role"] == "user"
    assert agent.history[2]["role"] == "assistant"

    # Assistant messages must be strings
    assert isinstance(agent.history[2]["content"], str)
    assert isinstance(agent.history[4]["content"], str)