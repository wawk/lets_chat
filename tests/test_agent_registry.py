import os
import uuid
import pytest

from agents.agent_registry import AgentRegistry
from agents.agent_factory import AgentFactory
from memory.memory_manager_v2 import MemoryManagerV2

TEST_DIR = "memory/agents"

def test_registry_can_add_agent():
    registry = AgentRegistry()
    factory = AgentFactory()

    agent = factory.create_agent()
    registry.add(agent)

    assert registry.get(agent.agent_id) is agent

def test_registry_lists_all_agents():
    registry = AgentRegistry()
    factory = AgentFactory()

    a1 = factory.create_agent()
    a2 = factory.create_agent()

    registry.add(a1)
    registry.add(a2)

    ids = registry.list_ids()
    assert a1.agent_id in ids
    assert a2.agent_id in ids

def test_registry_can_rename_agent():
    registry = AgentRegistry()
    factory = AgentFactory()

    agent = factory.create_agent()
    registry.add(agent)

    registry.rename(agent.agent_id, "Nova")

    data = agent.memory_manager.load()
    assert data["agent_name"] == "Nova"

def test_registry_can_delete_agent():
    registry = AgentRegistry()
    factory = AgentFactory()

    agent = factory.create_agent()
    registry.add(agent)

    registry.delete(agent.agent_id)

    assert registry.get(agent.agent_id) is None
    assert not os.path.exists(f"{TEST_DIR}/{agent.agent_id}.json")
    