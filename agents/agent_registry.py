import os

class AgentRegistry:
    def __init__(self):
        self._agents = {} # uuid -> Agent instance

    def add(self, agent):
        self._agents[agent.agent_id] = agent

    def get(self, agent_id):
        return self._agents.get(agent_id)

    def list_ids(self):
        return list(self._agents.keys())

    def rename(self, agent_id, new_name):
        agent = self.get(agent_id)
        if not agent:
            return False
        agent.memory_manager.update("agent_name", new_name)
        return True

    def delete(self, agent_id):
        agent = self.get(agent_id)
        if not agent:
            return False
        # Delete memory file
        path = agent.memory_manager.path
        if os.path.exists(path):
            os.remove(path)
        # Remove from registry
        del self._agents[agent_id]
        return True