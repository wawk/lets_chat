import os
from dotenv import load_dotenv
load_dotenv()
system_prompt = "You are a helpful friendly assistant."
from memory.memory_manager import MemoryManager
from llm.llm_wrapper import LLM
from agents.agent import Agent

def test_agent_real_llm_integration():
    # Use a known path for the test
    memory_manager = MemoryManager(path = "agent_memory.json")

    # Clean up any previous memory file
    if memory_manager.memory_file_exists():
        memory_manager.remove_memory()

    # Real LLM wrapper
    llm = LLM(provider="openai", model="gpt-4o-mini")

    agent = Agent(llm=llm, memory_manager=memory_manager)

    # Store memory
    ack = agent.handle_user_message("Remember that my favorite color is blue.")
    assert isinstance(ack, str)
    assert len(ack) > 0

    # Memory file should exist
    assert memory_manager.memory_file_exists()

    # Memory should contain the stored fact
    data = memory_manager.load_memory()
    assert data["favorite_color"] == "blue"

    # New agent should load memory
    llm2 = LLM(provider = "openai", model = "gpt-4o-mini")
    agent2 = Agent(llm=llm2, memory_manager = memory_manager)

    reply = agent2.handle_user_message("What is my favorite color?")

    # Basic correctness
    assert isinstance(reply, str)
    assert len(reply) > 0

    # The reply should mention the stored value
    assert "blue" in reply.lower()
    
    