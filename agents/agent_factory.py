import uuid
import os

from agents.agent import Agent

class AgentFactory:

    def create_agent(self, llm, memory_manager, agent_id, system_prompt=None):

        # Create Agent instance
        agent = Agent(
            llm=llm,
            agent_id=agent_id,
            memory_manager=memory_manager,
            system_prompt = system_prompt
        )

        return agent
