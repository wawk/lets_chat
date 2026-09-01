import re
import uuid
from enum import Enum

from agents.agent_factory import AgentFactory
from agents.agent_registry import AgentRegistry
from memory.memory_manager_v2 import MemoryManagerV2


class ManagerMode(Enum):
    MODERATED = "moderated"
    PARTY_LINE = "party_line"


class ManagerAgent:
    def __init__(self, llm=None):
        self.llm = llm                      # Jarvis' own LLM (optional fallback)
        self.factory = AgentFactory()       # Factory no longer owns an LLM
        self.registry = AgentRegistry()     # Tracks all agents
        self.mode = ManagerMode.MODERATED
        self.agent_id = str(uuid.uuid4())   # Jarvis' own ID
        self.active_agent_id = None         # Who currently has control

    # ----------------------------------------------------------------------
    # AGENT CREATION
    # ----------------------------------------------------------------------
    def spawn_agent(self, llm=None, name=None, system_prompt=None):
        """
        Create a new agent with:
        - its own UUID
        - its own MemoryManagerV2
        - an injected llm (or Jarvis' llm if none provided)
        - optional name + system prompt stored in memory
        """

        agent_id = str(uuid.uuid4())
        memory_manager = MemoryManagerV2(agent_id)

        # Decide which llm the agent gets
        agent_llm = llm if llm is not None else self.llm

        # Create agent through factory
        agent = self.factory.create_agent(
            llm=agent_llm,
            memory_manager=memory_manager,
            agent_id=agent_id,
            system_prompt=system_prompt
        )

        # Optional: store agent name in memory
        if name:
            memory_manager.update("agent_name", name)

        # Register agent so Jarvis can manage it
        self.registry.add(agent)

        return agent

    # ----------------------------------------------------------------------
    # RENAME AGENT
    # ----------------------------------------------------------------------
    def rename_agent(self, agent_id, name=None):
        agent = self.registry.get(agent_id)
        if agent is None:
            return f"I can't find an agent with id: {agent_id}"

        if not name:
            return "An actual name must be supplied to rename"

        agent.memory_manager.update("agent_name", name)
        return agent

    # ----------------------------------------------------------------------
    # SYSTEM PROMPT ASSIGNMENT
    # ----------------------------------------------------------------------
    def assign_system_prompt(self, agent_id, prompt):
        agent = self.registry.get(agent_id)

        if not agent:
            return f"No agent found with id: {agent_id}"
        if not prompt:
            return "Must supply a prompt string"

        data = agent.memory_manager.load()
        personality = data.get("personality", {})
        personality["system_prompt"] = prompt

        agent.memory_manager.update("personality", personality)

    # ----------------------------------------------------------------------
    # MODE NORMALIZATION + SETTING
    # ----------------------------------------------------------------------
    def normalize_mode(self, mode_str):
        ns = mode_str.lower()
        ns = re.sub(r"[\s\-_]+", "_", ns)
        ns = ns.strip("_")
        return ns

    def set_mode(self, mode_str):
        mode = self.normalize_mode(mode_str)
        try:
            self.mode = ManagerMode(mode).value
            return f"Mode set to {self.mode}"
        except ValueError:
            return f"mode: {mode} not a valid mode"

    # ----------------------------------------------------------------------
    # ROUTING
    # ----------------------------------------------------------------------
    def route_to_agent(self, agent_id, message_str):
        agent = self.registry.get(agent_id)
        if not agent:
            return f"No agent found with id: {agent_id}"
        if not message_str:
            return "No message found"

        reply = agent.handle_user_message(message_str)

        if isinstance(reply, dict) and "content" in reply:
            return reply["content"]

        return reply

    # ----------------------------------------------------------------------
    # CONTROL RETURN
    # ----------------------------------------------------------------------
    def return_control(self):
        self.active_agent_id = None
