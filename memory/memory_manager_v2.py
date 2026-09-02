import json
import os
import tempfile

class MemoryManagerV2:
    def __init__(self, agent_id, base_dir="memory"):
        self.agent_id = agent_id
        self.base_dir = base_dir
        self.agent_dir = os.path.join(self.base_dir, "agents")

        # Ensure directories exist
        os.makedirs(self.agent_dir, exist_ok=True)

    def get_memory_file_path(self):
        return os.path.join(self.agent_dir, f"{self.agent_id}.json")

    def load_memory(self):
        path = self.get_memory_file_path()
        if not os.path.exists(path):
            return {}

        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return {}  # safe fallback

    def save_memory(self, memory_dict):
        path = self.get_memory_file_path()

        # atomic write
        fd, temp_path = tempfile.mkstemp(dir=self.agent_dir)
        with os.fdopen(fd, "w") as tmp:
            json.dump(memory_dict, tmp, indent=2)

        os.replace(temp_path, path)

    def update_facts(self, key, value):
        memory = self.load_memory()
        memory[key] = value
        self.save_memory(memory)
        return memory

    def parse_memory_instruction(self, text):
        parts = text.lower().split()
        if "remember" not in parts or "is" not in parts:
            return None, None

        try:
            key_index = parts.index("remember") + 1
            is_index = parts.index("is")
            key = parts[key_index]
            value = parts[is_index + 1]
            return key, value
        except Exception:
            return None, None
