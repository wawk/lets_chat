import json
import os
from memory.memory_manager import MemoryManager

class Agent:
    def __init__(self, llm, system_prompt=None, memory_manager=None):
        self.llm = llm
        self.history = []
        self.memory_manager = memory_manager or MemoryManager()
        self.memory = self.memory_manager.load_memory()
        self.system_prompt = system_prompt

    def _prepare_messages(self, user_text):
        messages = []

        # 1. System prompt (personality)
        # if self.system_prompt:
        # 1. System prompt + emulation module
        if self.system_prompt:
            emulation_rules = (
                "Tone: warm, witty, curious, conversational."
                "Style: friendly, natural pacing, subtle humor, thoughtful follow-ups. "
                "Behaviour: maintain continuity, use memory naturally, stay consistent with personality."
            )
            messages.append({
                "role": "system",
                "content": f"{self.system_prompt}\n\n{emulation_rules}"
                # "content": self.system_prompt
            })

        # 2. Inject relevant memory
        relevant_memory = []
        for key, value in self.memory.items():
            if key.replace("_", " ") in user_text.lower():
                relevant_memory.append(f"{key}: {value}")

        if relevant_memory:
            messages.append({
                "role": "system",
                "content": "User memory: " + "; ".join(relevant_memory)
            })

        # 3. Conversation history
        for msg in self.history:
            messages.append(msg)

        # 4. New user message
        messages.append({
            "role": "user",
            "content": user_text
        })

        return messages

    def handle_user_message(self, text):

        # Add user message to history
        self.history.append({
            "role": "user",
            "content": text
        })

        # MEMORY FLAG DETECTION
        if "remember" in text.lower():
            key, value = self.memory_manager.parse_memory_instruction(text)
            if key and value:
                self.memory[key] = value
                self.memory_manager.save_memory(self.memory)
                reply = "Okay, I will remember that."
                self.history.append({"role": "assistant", "content": reply})
                return reply

        # Build full message context
        messages = self._prepare_messages(text)

        # NORMAL LLM FLOW
        reply = self.llm.invoke(messages)

        # Save assistant reply
        self.history.append({
            "role": "assistant",
            "content": reply
        })

        return reply
