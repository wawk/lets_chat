import openai

class LLM:
    def __init__(self, provider, model):
        self.provider = provider
        self.model = model

    def invoke(self, messages):
        if self.provider != "openai":
            raise ValueError("Unsupported provider")

        if not isinstance(messages, list):
            raise TypeError("messages must be a list")

        if len(messages) == 0:
            raise ValueError("messages cannot be empty")

        response = openai.chat.completions.create(
            model=self.model,
            messages=messages
        )

        msg = response.choices[0].message

        # Support both dict (mock) and object (real API)
        if isinstance(msg, dict):
            return msg["content"]

        else:
            return msg.content

        return response.choices[0].message["content"]
