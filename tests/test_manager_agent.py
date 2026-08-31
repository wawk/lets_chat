import pytest
from agents.agent_factory import AgentFactory
from agents.agent_registry import AgentRegistry
from agents.manager_agent import ManagerAgent

def test_jarvis_can_spawn_agent():
    jarvis = ManagerAgent()
    agent = jarvis.spawn_agent()

    assert agent.agent_id is not None
    assert jarvis.registry.get(agent.agent_id) is agent

def test_jarvis_can_spawn_agent_with_name():
    jarvis = ManagerAgent()
    agent = jarvis.spawn_agent(name = "Rachel")

    data = agent.memory_manager.load()
    assert data["agent_name"] == "Rachel"

def test_jarvis_can_rename_agent():
    jarvis = ManagerAgent()
    agent = jarvis.spawn_agent(name = "Alpha")
    jarvis.rename_agent(agent.agent_id, "Nova")
    data = agent.memory_manager.load()

    assert data["agent_name"] == "Nova"

def test_jarvis_can_assign_system_prompt():
    jarvis = ManagerAgent()
    agent = jarvis.spawn_agent()

    prompt = "You are a friendly research assistant."
    jarvis.assign_system_prompt(agent.agent_id, prompt)

    data = agent.memory_manager.load()
    assert data["personality"]["system_prompt"] == prompt

def test_jarvis_can_switch_modes():
    jarvis = ManagerAgent()

    jarvis.set_mode("party_line")
    assert jarvis.mode == "party_line"

    jarvis.set_mode("moderated")
    assert jarvis.mode == "moderated"

def test_jarvis_can_route_messages_to_agent():
    class FakeLLM:
        def invoke(self, messages):
            return {"content": "Hello from agent"}
    jarvis = ManagerAgent(llm=FakeLLM())
    agent = jarvis.spawn_agent(name="Echo")

    response = jarvis.route_to_agent(agent.agent_id, "Hello Echo")
    assert response == "Hello from agent"

def test_jarvis_returns_control_to_self():
    jarvis = ManagerAgent()
    jarvis.active_agent_id = "some-agent"
    jarvis.return_control()
    assert jarvis.active_agent_id is None
