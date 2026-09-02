import uuid
from agents.agent import Agent
from memory.memory_manager_v2 import MemoryManagerV2


class ManagerAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.agents = {}  # agent_id → Agent instance

    # ----------------------------------------------------------------------
    # SPAWN AGENT
    # ----------------------------------------------------------------------
    def spawn_agent(self, llm=None, name=None, system_prompt=None):
        agent_id = uuid.uuid4().hex
        memory_manager = MemoryManagerV2(agent_id)

        agent_llm = llm if llm is not None else self.llm

        agent = Agent(
            llm=agent_llm,
            memory_manager=memory_manager,
            agent_id=agent_id,
            system_prompt=system_prompt
        )

        # Store in registry
        self.agents[agent_id] = agent

        # Optional: store agent name in memory
        if name:
            memory_manager.update_facts("agent_name", name)

        return agent

    # ----------------------------------------------------------------------
    # RENAME AGENT
    # ----------------------------------------------------------------------
    def rename_agent(self, agent_id, name):
        if agent_id not in self.agents:
            raise KeyError(f"No agent found with id: {agent_id}")

        agent = self.agents[agent_id]
        agent.memory_manager.update_facts("agent_name", name)
        return agent

    # ----------------------------------------------------------------------
    # ASSIGN SYSTEM PROMPT
    # ----------------------------------------------------------------------
    def assign_system_prompt(self, agent_id, prompt):
        if agent_id not in self.agents:
            raise KeyError(f"No agent found with id: {agent_id}")

        agent = self.agents[agent_id]

        # Load existing personality block
        data = agent.memory_manager.load_memory()
        personality = data.get("personality", {})
        personality["system_prompt"] = prompt

        # Save updated personality
        agent.memory_manager.save_memory({**data, "personality": personality})

        # Update agent runtime prompt
        agent.system_prompt = prompt

    # ----------------------------------------------------------------------
    # ROUTE MESSAGE TO AGENT
    # ----------------------------------------------------------------------
    def handle_message(self, agent_id, text):
        if agent_id not in self.agents:
            raise KeyError(f"No agent found with id: {agent_id}")

        agent = self.agents[agent_id]
        return agent.handle_user_message(text)
