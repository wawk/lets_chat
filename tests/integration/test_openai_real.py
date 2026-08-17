import os
from llm.llm_wrapper import LLM
from dotenv import load_dotenv
load_dotenv()
def test_real_openai_call():
    assert "OPENAI_API_KEY" in os.environ

    llm = LLM(provider="openai", model="gpt-4o-mini")
    messages = [{"role": "user", "content": "Hello"}]

    reply = llm.invoke(messages)

    assert isinstance(reply, str)
    assert len(reply) > 0
