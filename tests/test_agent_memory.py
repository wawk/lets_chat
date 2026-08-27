import os
import json
from unittest.mock import MagicMock
from core.agent import Agent
from memory.memory_manager import MemoryManager


def test_agent_memory_persistence():
    memory_manager = MemoryManager()
    # Clean up any previous memory file
    if memory_manager.memory_file_exists():
        memory_manager.remove_memory()

    llm = MagicMock()
    llm.invoke.return_value = "ignored"
    # llm.invoke.side_effect = [
    #     "Okay, I will rember that.",
    #     "Your favorite color is blue."
    # ]

    agent = Agent(llm=llm, memory_manager=memory_manager)

    # User tells the agent to remember something
    agent.handle_user_message("Remember that my favorite color is blue")

    # Memory file should now exist
    #assert os.path.exists("agent_memory.json")
    assert memory_manager.memory_file_exists()

    # Memory file sshould contain the stored fact
    # with open(memory_manager.path, "r") as f:
    #     data = json.load(f)
    data = memory_manager.load_memory()
    assert data["favorite_color"] == "blue"

    # Create a new agent instance to test loading
    llm2 = MagicMock()
    llm2.invoke.return_value = "Your favorite color is blue"

    agent2 = Agent(llm = llm2)

    # Agent should load memory and use it
    reply = agent2.handle_user_message("What is my favorite color?")
    assert "blue" in reply.lower()