import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"


class HistoryManager:
    def __init__(self):
        self.history = self.load()

    def load(self):
        if not os.path.exists(HISTORY_FILE):
            return []

        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки истории: {e}")
            return []

    def save(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Ошибка сохранения истории: {e}")

    def add_record(self, pdf_name, tag_no, stats):
        record = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pdf_name": pdf_name,
            "tag_no": tag_no or "N/A",
            "stats": stats
        }

        self.history.insert(0, record)

        if len(self.history) > 100:
            self.history = self.history[:100]

        self.save()

    def get_all(self):
        return self.history

    def clear(self):
        self.history = []
        self.save()
