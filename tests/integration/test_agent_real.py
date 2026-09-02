import os
import uuid
from agents.manager_agent import ManagerAgent
from agents.agent import Agent
from memory.memory_manager_v2 import MemoryManagerV2
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


def test_agent_real_end_to_end():
    """
    Full real‑LLM integration test using GPT‑4o‑mini.
    Covers:
    - ManagerAgent spawning
    - Agent construction
    - UUID identity
    - System prompt propagation
    - Real LLM invocation
    - History tracking
    - Memory instruction persistence
    - Multi‑turn conversation
    """

    # Real OpenAI client
    client = OpenAI()

    # ManagerAgent uses real LLM
    manager = ManagerAgent(llm=client)

    # Spawn agent with system prompt
    agent = manager.spawn_agent(system_prompt="You are helpful")

    # Basic agent properties
    assert isinstance(agent, Agent)
    assert len(agent.agent_id) == 32
    assert agent.agent_id in manager.agents
    assert agent.system_prompt == "You are helpful"

    # First message
    reply = manager.handle_message(agent.agent_id, "Hello agent")
    assert isinstance(reply, str)
    assert len(reply) > 0

    # History should contain user + assistant
    assert agent.history[-2]["content"] == "Hello agent"
    assert isinstance(agent.history[-1]["content"], str)

    # Memory instruction
    reply2 = manager.handle_message(agent.agent_id, "remember favorite_color is blue")
    assert reply2 == "Okay, I will remember that."

    # Memory persisted
    data = agent.memory_manager.load_memory()
    assert data["favorite_color"] == "blue"

    # Multi‑turn conversation
    reply3 = manager.handle_message(agent.agent_id, "What is my favorite color?")
    assert isinstance(reply3, str)
    assert len(reply3) > 0

    # History grows correctly
    assert len(agent.history) >= 5
