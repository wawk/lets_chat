from core.agent import Agent
from llm.llm_wrapper import LLM
from memory.memory_manager import MemoryManager

def main():
    # 1. Initialize LLM
    llm = LLM(provider="openai", model="gpt-4o")

    # 2. Initialize memory manager
    memory_manager = MemoryManager()

    # 3. Define your agent's personality
    system_prompt = (
        "You are LetsChat, a warm, witty, curious personal AI agent. "
        "You maintain continuity, remember user facts, and respond with personality. "
        "You are not a raw LLM—you are an agent with identity, memory, and conversational style."
    )

    # 4. Create the agent
    agent = Agent(
        llm=llm,
        system_prompt=system_prompt,
        memory_manager=memory_manager
    )

    print("LetsChat Agent Ready. Type 'exit' to quit.\n")

    # 5. REPL loop
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        reply = agent.handle_user_message(user_input)
        print("Agent:", reply)

if __name__ == "__main__":
    main()
