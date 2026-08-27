import json
import os
import re
import sys
from dotenv import load_dotenv
load_dotenv()
class MemoryManager:
    def __init__(self, path=None):
        self.path = path or os.getenv("AI_MEMORY_PATH")
        self.directory = os.path.dirname(self.path)

    def memory_file_exists(self):
        return os.path.exists(self.path)

    def ensure_memory_directory(self):
        if self.directory and not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def create_memory_file(self):
        self.ensure_memory_directory()
        try:
            with open(self.path, "w") as f:
                json.dump({}, f, indent=4)
        except Exception as e:
            sys.exit(f"Error creating {self.path}: {e}")

    def load_memory(self):
        if self.memory_file_exists():
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except Exception as e:
                sys.exit(f"Error loading {self.path}: {e}")

        # File does not exist — create it and return empty dict
        self.create_memory_file()
        return {}

    def save_memory(self, memory):
        self.ensure_memory_directory()
        try:
            with open(self.path, "w") as f:
                json.dump(memory, f, indent=4)
        except Exception as e:
            sys.exit(f"Error saving memory to {self.path}: {e}")

    def remove_memory(self):
        if self.memory_file_exists():
            os.remove(self.path)

    def parse_memory_instruction(self, text):
        # Normalize
        t = text.lower().strip()
        t = t.replace(".", "").replace("?", "")

        # Remove leading "remember" or "remember that or this"
        t = re.sub(r"^remember(?:\s+(?:that|this))?\s*", "", t)

        # Split on "is"
        if " is " in t:
            key_part, value_part = t.split(" is ", 1)
        else:
            # If no "is" we can't parse reliably
            return None, None

        #Clean Key
        key = key_part.strip()

        # Remove leading "my " or "i "
        key = re.sub(r"^(my|i)\s+", "", key)
        # Convert to snake_case
        key = key.replace(" ", "_")

        #Clean Value
        value = value_part.strip()

        return key, value