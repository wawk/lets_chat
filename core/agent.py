
class Agent:
    def __init__(self, llm, system_prompt=None):
        self.llm = llm
        self.history = []
        self.system_prompt = system_prompt
        if self.system_prompt:
                    self.history.append({
                        "role": "system",
                        "content": self.system_prompt
                    })
       

    def handle_user_message(self, text):
        
        messages = []
        
        self.history.append({
            "role": "user",
            "content": text
        })

        reply = self.llm.invoke(self.history.copy())
        self.history.append({
              "role": "assistant",
              "content": reply
        })
        return reply
