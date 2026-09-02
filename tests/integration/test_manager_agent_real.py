import os
import uuid
from agents.manager_agent import ManagerAgent
from agents.agent import Agent
from memory.memory_manager_v2 import MemoryManagerV2
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def test_manager_agent_real_end_to_end():
    client = OpenAI()
    # Create Manager Agent with real OpenAI client
    manager = ManagerAgent(llm = client)

    # Spawn two agents with different system prompts
    agent_alpha = manager.spawn_agent(system_prompt = " You are the first of your kind and helpful, courteous, and friendly")
    agent_beta = manager.spawn_agent(system_prompt = " You are number 2 but very friendly and helpful")


    # Send a message to agent A
    replyA = manager.handle_message(agent_alpha.agent_id, "Hello Alpha")

    # Send a message to agent B
    replyB = manager.handle_message(agent_beta.agent_id, "Hello Beta")

    # Memory persistence for each agent
    replyAM = manager.handle_message(agent_alpha.agent_id, "remember favorite_color is blue")
    replyBM = manager.handle_message(agent_beta.agent_id, "remember  favorite_hoby is ai-coding")
    dataA = agent_alpha.memory_manager.load_memory()
    dataB = agent_beta.memory_manager.load_memory()
        

    # Assert their histories differ
    assert agent_alpha.history != agent_beta.history

    # Assert their memories differ
    # This also verifies that agents are routed correctly
    assert dataA != dataB
    

    # Assert each agent's system prompt is preserved
    assert agent_alpha.system_prompt == " You are the first of your kind and helpful, courteous, and friendly"
    assert agent_beta.system_prompt ==  " You are number 2 but very friendly and helpful"
    # Assert each agent's reply is a string
    assert all(isinstance(r["content"], str) for r in agent_alpha.history[-2:])
    assert all(isinstance(r["content"], str) for r in agent_beta.history[-2:])

    # Assert the real LLM is invoked twice
    assert isinstance(replyAM, str) and len(replyAM)  > 1
    assert isinstance(replyBM, str) and len(replyBM)  > 1
    # Assert the registry contains both agents
    assert agent_alpha.agent_id in manager.agents
    assert agent_beta.agent_id in manager.agents
    assert agent_alpha.agent_id != agent_beta.agent_id
    
