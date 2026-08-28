import os 
import uuid
import pytest
from agents.agent_factory import AgentFactory
from memory.memory_manager_v2 import MemoryManagerV2
from agents.agent import Agent
TEST_DIR = "memory_agents"

def test_agent_factory_creates_agent_with_uuid():
    factory = AgentFactory()
    agent = factory.create_agent()

    assert isinstance(agent.agent_id, str)
    assert len(agent.agent_id) > 0

def test_agent_factory_creates_unique_memory_file():
    factory = AgentFactory()
    agent = factory.create_agent()

    assert isinstance(agent.memory_manager, MemoryManagerV2)

def test_agent_factory_initializes_agent_with_default_personality():
    factory = AgentFactory()
    agent = factory.create_agent()

    data = agent.memory_manager.load()
    assert data["personality"] == {}, "Default personality should be empty"

def test_agent_factory_allows_custom_llm():
    class FakeLLM:
        def invoke(self, messages):
            return "ok"
    llm = FakeLLM()
    factory = AgentFactory(llm=llm)
    agent = factory.create_agent()
    assert agent.llm is llm
              
