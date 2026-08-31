import re
import uuid
from agents.agent_factory import AgentFactory
from agents.agent_registry import AgentRegistry
from memory.memory_manager_v2 import MemoryManagerV2
from enum import Enum

class ManagerMode(Enum):
     MODERATED = "moderated"
     PARTY_LINE = "party_line"

class ManagerAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.factory = AgentFactory()
        self.registry = AgentRegistry()
        self.mode = ManagerMode.MODERATED
        self.agent_id = str(uuid.uuid4())
        self.active_agent_id = None

    def spawn_agent(self, llm=None, name=None, system_prompt=None):
            # 1 Create a new agent using the factory
            agent = self.factory.create_agent()

            # 2 If a name was provided, store it in the agent's memory
            if name:
                agent.memory_manager.update("agent_name", name)

            # 3 Register the agentso Jarvis can manager it
            self.registry.add(agent)

            # 4 Return the agent instance
            return agent

    def rename_agent(self, agent_id, name=None):
         # Check the registry for the agent id
         agent = self.registry.get(agent_id)
         # If no agent found with that agent id  return message
         if agent is None:
              return f"I can't find an agent with id: {agent_id}"
        # check if a actual name was passed in if not return message
         if name is None:
              return "An actual name must be supplied to rename"

        # Update the agent memory with new name
         agent.memory_manager.update("agent_name", name)
        # return the updated agent
         return agent

    def assign_system_prompt(self, agent_id, prompt):
         agent = self.registry.get(agent_id)
         
         if not agent:
              return f"No agent found with id: {agent_id}"
         if not prompt:
              return "Must supply a prompt string"
         data = agent.memory_manager.load()
         data["personality"]["system_prompt"] = prompt
         agent.memory_manager.update("personality", data["personality"])

    def normalize_mode(self, mode_str):
         # Lowercase the input
         ns = mode_str.lower()
         # Replace ANY sequences of spaces, hyphens, or underscores with a single underscore
         ns = re.sub(r"[\s\-_]+", "_", ns)
         # Strip leading and trailing underscores
         ns = ns.strip("_")
         return ns

    def set_mode(self, mode_str):
         # Normalize string input
         mode = self.normalize_mode(mode_str)
         try:
              self.mode = ManagerMode(mode).value
              return f"Mode set to {self.mode}"
         except ValueError:
             return  f" mode: {mode} not a valid mode"

    def  route_to_agent(self,agent_id, message_str):
         agent = self.registry.get(agent_id)
         if not agent:
               return f"No agent found with id: {agent_id}"
         if not message_str:
              return "No message found"
         reply = agent.handle_user_message(message_str)
         if isinstance(reply, dict) and "content" in reply:
              return reply["content"]
         return reply

    def return_control(self):
         # We are doing on thing and one hting only here
         # we are setting the value of the active_agent_id back to jarvis
         self.active_agent_id = None
              



         