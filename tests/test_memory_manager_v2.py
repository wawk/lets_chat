import os
import uuid
import json
import pytest
from memory.memory_manager_v2 import MemoryManagerV2

TEST_DIR = "memory/agents"

def test_memory_manager_creates_file_if_missing():
    agent_id = uuid.uuid4().hex
    path = f"{TEST_DIR}/{agent_id}.json"

    # Ensure file does not exist
    if os.path.exists(path):
        os.remove(path)
    mm = MemoryManagerV2(path)

    assert os.path.exists(path), "MemoryManagerV2 should create the file if missing"

def test_memory_manager_loads_empty_structure_initially():
    agent_id = uuid.uuid4().hex
    path = f"{TEST_DIR}/{agent_id}.json"
    if os.path.exists(path):
        os.remove(path)
    mm = MemoryManagerV2(path)
    data = mm.load()

    assert isinstance(data, dict)
    assert data["agent_id"] == agent_id
    assert data["facts"] == {}
    assert data["personality"] == {}
    assert data["user_name"] is None
    assert data["agent_name"] is None

def test_memory_manager_saves_and_loads_updates():
    agent_id = uuid.uuid4().hex
    path = f"{TEST_DIR}/{agent_id}.json"

    if os.path.exists(path):
        os.remove(path)
    mm = MemoryManagerV2(path)

    mm.update("agent_name", "Bob")
    mm.update("user_name", "Steve")
    mm.update_facts("favorite_color", "blue")

    data = mm.load()


    assert data["agent_name"] == "Bob"
    assert data["user_name"] == "Steve"
    assert data["facts"]["favorite_color"] == "blue"

    def test_memory_manager_persists_across_instances():

        agent_id = uuid.uuid4().hex
        path = f"{TEST_DIR}/ {agent_id}.json"

        if os.path.exists(path):
            os.remove(path)
        mm1 = MemoryManagerV2(path)
        mm1.update("agent_name", "Eve")
        mm1.update("mood", "curious")

        mm2 = MemoryManagerV2(path)
        data = mm2.load()

        assert data["agent_name"] == "Eve"
        assert data["facts"]["mood"] == "curious"


