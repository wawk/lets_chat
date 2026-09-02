import uuid
from agents.manager_agent import ManagerAgent
from agents.agent import Agent

class FakeLLM:
    def __init__(self):
        self.last_messages = None

    def invoke(self, messages):
        self.last_messages = messages
        return {"content": "LLM reply"}

def test_manager_agent_spawns_agents_with_uuid():
    llm = FakeLLM()
    manager = ManagerAgent(llm=llm)

    agent = manager.spawn_agent(system_prompt="You are helpful")

    assert isinstance(agent, Agent)
    assert agent.agent_id in manager.agents
    assert len(agent.agent_id) == 32  # UUID hex
    assert agent.system_prompt == "You are helpful"

def test_manager_agent_injects_memory_manager_v2():
    llm = FakeLLM()
    manager = ManagerAgent(llm=llm)

    agent = manager.spawn_agent(system_prompt="test")

    # MemoryManagerV2 should exist and be bound to this agent
    assert agent.memory_manager is not None
    assert agent.memory_manager.agent_id == agent.agent_id

def test_manager_agent_routes_messages_to_agent():
    llm = FakeLLM()
    manager = ManagerAgent(llm=llm)

    agent = manager.spawn_agent(system_prompt="test")

    reply = manager.handle_message(agent.agent_id, "Hello agent")

    assert reply == "LLM reply"
    assert llm.last_messages is not None
    assert llm.last_messages[-1]["content"] == "Hello agent"

def test_manager_agent_tracks_multiple_agents():
    llm = FakeLLM()
    manager = ManagerAgent(llm=llm)

    a1 = manager.spawn_agent(system_prompt="A1")
    a2 = manager.spawn_agent(system_prompt="A2")

    assert a1.agent_id in manager.agents
    assert a2.agent_id in manager.agents
    assert a1.agent_id != a2.agent_id

def test_manager_agent_raises_for_unknown_agent():
    llm = FakeLLM()
    manager = ManagerAgent(llm=llm)

    try:
        manager.handle_message("unknown_id", "Hello")
        assert False, "Expected KeyError for unknown agent"
    except KeyError:
        assert True

def test_manager_agent_passes_system_prompt_to_agent():
    llm = FakeLLM()
    manager = ManagerAgent(llm=llm)

    agent = manager.spawn_agent(system_prompt="You are a test agent.")

    # Agent.prepare_messages should include system prompt first
    manager.handle_message(agent.agent_id, "Ping")

    system_msg = llm.last_messages[0]
    assert system_msg["role"] == "system"
    assert system_msg["content"] == "You are a test agent."
