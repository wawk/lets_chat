from core.agent import Agent
from llm.llm_wrapper import LLM
from memory.memory_manager import MemoryManager

class FakeLLM:
    def invoke(self,messages):
        # Return the last user message so we can inspect. the system prompt
        return f"LLM saw: {messages[0]['content']}"

def test_personality_injection():
    llm = FakeLLM()
    memory = MemoryManager()
    system_prompt = " You are LetsChat a warm wittly curious personal AI agent."

    agent = Agent(llm=llm, system_prompt=system_prompt, memory_manager = memory)
    reply = agent.handle_user_message("hello")

    assert "warm, witty, curious" in reply
