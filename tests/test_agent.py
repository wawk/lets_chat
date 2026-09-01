from agents.agent import Agent

class FakeLLM:
        def invoke(self, messages):
            return "ok"

# Test History

def test_agent_appends_user_messages():
    agent = Agent(
        llm = FakeLLM(),
        memory_manager=None,
        agent_id="test_agent",
        system_prompt = None
    )
    agent.handle_user_message("Hello World.")

    # Assert
    assert len(agent.history) == 2
    assert agent.history[0]["role"] == "user"
    assert agent.history[0]["content"] == "Hello World."

def test_agent_appends_assistant_messages():
    agent = Agent(
        llm = FakeLLM(),
        memory_manager=None,
        agent_id="test_agent",
        system_prompt = None
    )
    agent.handle_user_message("Hi")
    assert agent.history[1]["role"] == "assistant"
    assert agent.history[1]["content"] == "ok"

def test_agent_preserves_history_order():
    agent = Agent(
           llm = FakeLLM(),
           memory_manager=None,
           agent_id="test_agent",
           system_prompt = None
    )
    agent.handle_user_message("First")
    agent.handle_user_message("Second")

    assert agent.history[0]["role"] == "user"
    assert agent.history[0]["content"] == "First"
    assert agent.history[1]["role"] == "assistant"
    assert agent.history[1]["content"] == "ok"
    assert agent.history[2]["role"] == "user"
    assert agent.history[2]["content"] == "Second"
    assert agent.history[3]["role"] == "assistant"
    assert agent.history[3]["content"] == "ok"  

# Test Memory Instructions
def test_agent_updates_memory_on_remember():
     # Fake memory manager to capture updates
    class FakeMemoryManager:
            def __init__(self):
               self.updated = {}
            def load_memory(self):
                return {}  # Agent expects this
            def update_facts(self, key, value):
                 self.updated[key] = value
            def save_memory(self, memory):
                pass  # Agent will call this; no-op is fine
            def parse_memory_instruction(self, text):
                # Minimal parser for the test
                # "remember favorite_color is blue"
                parts = text.split()
                key = parts[1]
                value = parts[3]
                return key, value
    class FakeLLM:
         def invoke(self, messages):
              raise AssertionError("LLM should NOT be called for memory instructions")
    memory = FakeMemoryManager()

    agent = Agent(
         llm = FakeLLM(),
         memory_manager = memory,
         agent_id = "test_agent",
         system_prompt = None

    )

    reply = agent.handle_user_message("remember favorite_color is blue")

    # Memory should be updated
    assert memory.updated["favorite_color"] == "blue"

    # Agent should return confirmation
    assert reply == "Okay, I will remember that."

    # Confirmation should be appended to history
    assert agent.history[-1]["role"] == "assistant"
    assert agent.history[-1]["content"] == "Okay, I will remember that."

# Test PrepareMessages

# Test LLMInvocation