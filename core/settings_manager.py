import json
import os
import copy

DEFAULT_SETTINGS = {
    "server_url": "http://10.128.128.203:4181",
    "api_key": "",
    "language": "EN",
    "rendering_mode": "remote"
}

class SettingsManager:
    def __init__(self, config_path="config.json"):
        # For packaged apps, we must write to user home instead of current dir
        app_dir = os.path.expanduser("~/.plantuml-client")
        os.makedirs(app_dir, exist_ok=True)
        self.config_path = os.path.join(app_dir, config_path)
        self.settings = copy.deepcopy(DEFAULT_SETTINGS)
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                try:
                    loaded = json.load(f)
                    self._migrate(loaded)
                except json.JSONDecodeError:
                    pass

    def _migrate(self, loaded_settings):
        # Migration process based on TECH_STACK.md
        for key, default_val in DEFAULT_SETTINGS.items():
            if key in loaded_settings:
                self.settings[key] = loaded_settings[key]
            else:
                self.settings[key] = default_val
        self.save()

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)
