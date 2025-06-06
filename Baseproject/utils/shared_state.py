# utils/shared_state.py

import json
import os

class SharedState:
    def __init__(self, filename="variables.json"):
        self._data = {}
        self.filename = filename
        self.load()

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def all(self):
        return dict(self._data)

    def clear(self):
        self._data.clear()
        self.save()

    def save(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            print(f"Failed to save variables: {e}")

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self._data = json.load(f)
            except Exception as e:
                print(f"Failed to load variables: {e}")
                self._data = {}

# Singleton instance
state = SharedState()
