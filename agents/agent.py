
class Agent:
    def __init__(self, llm, memory_manager, agent_id, system_prompt=None):
        self.llm = llm
        self.history = []
        self.agent_id = agent_id
        self.memory_manager = memory_manager
        self.memory = self.memory_manager.load_memory() if memory_manager else {}
        self.system_prompt = system_prompt

    def _prepare_messages(self, user_text):
        messages = []

        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })

        # Conversation history
        for msg in self.history:
            messages.append(msg)

        # New user message
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
                self.memory_manager.update_facts(key,value)
                reply = "Okay, I will remember that."
                self.history.append({"role": "assistant", "content": reply})
                return reply

        # Build full message context
        messages = self._prepare_messages(text)

        # NORMAL LLM FLOW
        if hasattr(self.llm, "invoke"):
            # FakeLLM or custom LLM wrapper
            reply = self.llm.invoke(messages)
            reply_text = reply["content"] if isinstance(reply, dict) else reply
        else:
            # Real OpenAI client
            response = self.llm.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            reply_text = response.choices[0].message.content

        # Save assistant reply (string only)
        self.history.append({
            "role": "assistant",
            "content": reply_text
        })

        return reply_text