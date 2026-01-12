import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "api_endpoint": "http://localhost:8000",
    "pinned_files": {
        "bom_excel": None,
        "manager_excel": None
    },
    "last_bom_sheet_index": 0
}


class ConfigManager:
    def __init__(self):
        self.config = self.load()

    def load(self):
        if not os.path.exists(CONFIG_FILE):
            self.save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки config: {e}")
            return DEFAULT_CONFIG.copy()

    def save(self, config=None):
        if config is None:
            config = self.config

        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Ошибка сохранения config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()

    def get_pinned_file(self, file_type):
        return self.config.get("pinned_files", {}).get(file_type)

    def set_pinned_file(self, file_type, filepath):
        if "pinned_files" not in self.config:
            self.config["pinned_files"] = {}
        self.config["pinned_files"][file_type] = filepath
        self.save()

    def get_api_endpoint(self):
        return self.config.get("api_endpoint", "http://localhost:8000")

    def set_api_endpoint(self, endpoint):
        self.config["api_endpoint"] = endpoint
        self.save()
