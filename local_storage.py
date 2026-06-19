import json
import os


class LocalStorage:
    def __init__(self, filename="data.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump({}, file)

    def save(self, key, data):
        try:
            with open(self.filename, "r") as file:
                content = json.load(file)
            content[key] = data
            with open(self.filename, "w") as file:
                json.dump(content, file, indent=4)
        except Exception:
            raise IOError("Error saving data.")

    def load(self, key):
        try:
            with open(self.filename, "r") as file:
                content = json.load(file)
            return content.get(key)
        except Exception:
            raise IOError("Error loading data.")

    def load_all(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except Exception:
            return {}
