import os
import json
import shutil
from memory.memory_manager_v2 import MemoryManagerV2

TEST_DIR = "test_memory"

def setup_function():
    # Clean test directory before each test
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR, exist_ok=True)

def test_load_memory_returns_empty_when_file_missing():
    mm = MemoryManagerV2(agent_id="agent123", base_dir=TEST_DIR)

    memory = mm.load_memory()

    assert memory == {}
    assert os.path.exists(os.path.join(TEST_DIR, "agents"))

def test_save_memory_creates_file():
    mm = MemoryManagerV2(agent_id="agent123", base_dir=TEST_DIR)

    mm.save_memory({"foo": "bar"})

    path = os.path.join(TEST_DIR, "agents", "agent123.json")
    assert os.path.exists(path)

    with open(path, "r") as f:
        data = json.load(f)

    assert data["foo"] == "bar"

def test_update_facts_persists_changes():
    mm = MemoryManagerV2(agent_id="agent123", base_dir=TEST_DIR)

    mm.update_facts("favorite_color", "blue")

    path = os.path.join(TEST_DIR, "agents", "agent123.json")
    with open(path, "r") as f:
        data = json.load(f)

    assert data["favorite_color"] == "blue"

def test_update_facts_merges_existing_memory():
    mm = MemoryManagerV2(agent_id="agent123", base_dir=TEST_DIR)

    mm.save_memory({"favorite_color": "blue"})
    mm.update_facts("pet", "dog")

    memory = mm.load_memory()

    assert memory["favorite_color"] == "blue"
    assert memory["pet"] == "dog"

def test_parse_memory_instruction_basic():
    mm = MemoryManagerV2(agent_id="agent123", base_dir=TEST_DIR)

    key, value = mm.parse_memory_instruction("remember favorite_color is blue")

    assert key == "favorite_color"
    assert value == "blue"

def test_parse_memory_instruction_invalid():
    mm = MemoryManagerV2(agent_id="agent123", base_dir=TEST_DIR)

    key, value = mm.parse_memory_instruction("do not remember anything")

    assert key is None
    assert value is None

def test_atomic_write_creates_valid_json():
    mm = MemoryManagerV2(agent_id="agent123", base_dir=TEST_DIR)

    mm.save_memory({"x": 1})

    path = os.path.join(TEST_DIR, "agents", "agent123.json")

    # File must contain valid JSON even if atomic write used temp file
    with open(path, "r") as f:
        data = json.load(f)

    assert data["x"] == 1
