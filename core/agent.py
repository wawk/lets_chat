
class Agent:
    def __init__(self, llm, system_prompt=None):
        self.llm = llm
        self.system_prompt = system_prompt

    def handle_user_message(self, text):
        messages = []
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        messages.append({
            "role": "user",
            "content": text
        })
       
        return self.llm.invoke(messages)
