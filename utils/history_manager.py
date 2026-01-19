"""
Менеджер для управления историей парсингов
"""
import json
import os
from datetime import datetime


class HistoryManager:
    def __init__(self, history_file="history.json"):
        self.history_file = history_file
        self.history = self.load()
    
    def load(self):
        """Загружает историю из файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save(self):
        """Сохраняет историю в файл"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def add_record(self, pdf_name, tag_no, customer, project, stats):
        """
        Добавляет новую запись в историю
        
        Args:
            pdf_name: имя PDF файла
            tag_no: TAG номер
            customer: заказчик
            project: проект/локация
            stats: статистика {"total": int, "equal": int, "notEqual": int, "new": int}
        """
        record = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pdf_name": pdf_name,
            "tag_no": tag_no if tag_no else "N/A",
            "customer": customer if customer else "N/A",
            "project": project if project else "N/A",
            "stats": stats
        }
        
        self.history.insert(0, record)  # Добавляем в начало
        
        # Ограничиваем историю 100 записями
        if len(self.history) > 100:
            self.history = self.history[:100]
        
        self.save()
    
    def get_all(self):
        """Возвращает всю историю"""
        return self.history
    
    def clear(self):
        """Очищает всю историю"""
        self.history = []
        self.save()
