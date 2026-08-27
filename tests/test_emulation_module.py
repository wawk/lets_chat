from core.agent import Agent
from memory.memory_manager import MemoryManager

class FakeLLM:
    def invoke(self, messages):
        # Return the system messag so we cn inspect it
        return messages[0]["content"]

def test_emulation_module_injection():
        llm = FakeLLM()
        memory = MemoryManager()

        system_prompt = "You are LetsChat."

        agent = Agent(llm=llm, system_prompt=system_prompt, memory_manager= memory)

        reply = agent.handle_user_message("hello")

        # The emulation module should inject tone + style rules
        assert "tone:" in reply.lower()
        assert "style:" in reply.lower()
        assert "behaviour:" in reply.lower()
