
import os
import json
import uuid


class MemoryManagerV2:
    def __init__(self,path):
        self.path = path
        self.agent_id = os.path.splitext(os.path.basename(path))[0]

        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Create file if missing
        if not os.path.exists(path):
            self.initialize_file()

    def initialize_file(self):
            data = {
                "agent_id": self.agent_id,
                "agent_name": None,
                "user_name": None,
                "personality": {},
                "facts": {}
            }
            self._save(data)

    def _save(self,data):
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)

    def load(self):
            with open(self.path, "r") as f:
                return json.load(f)
    def update(self, key, value):
          data = self.load()
          data[key] = value
          self._save(data)

    def update_facts(self, key, value):
            data = self.load()
            data['facts'][key] = value
           
            self._save(data)
