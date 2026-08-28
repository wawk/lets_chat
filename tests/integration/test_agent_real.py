import os
from dotenv import load_dotenv
load_dotenv()

from llm.llm_wrapper import LLM
from agents.agent import Agent
system_prompt = "You are a helpful friendly assistant."
def test_agent_real_openai_call():
    assert "OPENAI_API_KEY" in os.environ

    llm = LLM(provider="openai", model="gpt-4o-mini")
    agent = Agent(llm=llm, system_prompt = system_prompt)

    reply = agent.handle_user_message("Hello from the integration test!")

    # Basic correctness checks
    assert isinstance(reply, str)
    assert len(reply) > 0

    # Agent should have stored system + user message
    assert agent.history[0]["role"] == "system"
    assert agent.history[1]["role"] == "user"