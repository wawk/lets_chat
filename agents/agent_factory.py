import uuid
import os

from memory.memory_manager_v2 import MemoryManagerV2
from agents.agent import Agent

class AgentFactory:
    def __init__(self, llm=None):
        self.llm = llm

    def create_agent(self):
        # 1. Generate UUID
        agent_id = uuid.uuid4().hex

        # 2. Build memory path
        memory_path = f"memory/agents/{agent_id}.json"

        # 3. Create MemoryManagerV2
        memory_manager = MemoryManagerV2(memory_path)

        # 4. Create Agent instance
        agent = Agent(
            llm=self.llm,
            agent_id=agent_id,
            memory_manager=memory_manager
        )

        return agent
