from agents.agent_factory import AgentFactory
from agents.agent_registry import AgentRegistry

class ManagerAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.factory = AgentFactory(llm=self.llm)
        self.registry = AgentRegistry()
        self.mode = "moderated"
        self.active_agent_id = None

    def spawn_agent(self, name=None):
        if not name:
            name = "New Agent"
        agent = self.factory(llm=llm)
        self.registry.add(agent)
        return agent