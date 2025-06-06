import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

class Config:
    _instance = None

    DEFAULTS = {
    "log_file_name": "status_log.txt",
    "log_everything": True,
    "log_level": 3,
    "window_geometry": "800x600"
}


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        if not os.path.exists(CONFIG_PATH):
            self._create_default_config()

        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)

        self.log_file_name = data.get("log_file_name", self.DEFAULTS["log_file_name"])
        self.log_everything = data.get("log_everything", self.DEFAULTS["log_everything"])
        self.log_level = data.get("log_level", self.DEFAULTS["log_level"])
        self.window_geometry = data.get("window_geometry", self.DEFAULTS["window_geometry"])



    def _create_default_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.DEFAULTS, f, indent=4)

    def save(self):
        data = {
            "log_file_name": self.log_file_name,
            "log_everything": self.log_everything,
            "log_level": self.log_level,
            "window_geometry": self.window_geometry,
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)
