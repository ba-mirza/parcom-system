"""
Страница истории парсингов
"""
import customtkinter as ctk
from tkinter import ttk, messagebox
import theme as th


class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, history_manager, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.history_manager = history_manager
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # ===== ЗАГОЛОВОК =====
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=th.SPACING_2XL, pady=(th.SPACING_2XL, th.SPACING_MD), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Parsing History",
            font=ctk.CTkFont(size=th.FONT_SIZE_2XL, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        title_label.grid(row=0, column=0, padx=0, sticky="w")
        
        # Кнопки
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=0, sticky="e")
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            width=100,
            fg_color=th.ACCENT_PRIMARY,
            hover_color=th.ACCENT_HOVER,
            command=self.refresh_history
        )
        refresh_btn.pack(side="left", padx=th.SPACING_SM)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear All",
            width=100,
            fg_color=th.ERROR,
            hover_color=th.ERROR_HOVER,
            command=self.clear_history
        )
        clear_btn.pack(side="left", padx=0)
        
        # ===== ТАБЛИЦА =====
        table_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT
        )
        table_frame.grid(row=1, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_2XL), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Treeview
        style = ttk.Style()
        style.theme_use('default')
        
        # Динамические цвета для Treeview
        bg_color = "#f5f5f5" if ctk.get_appearance_mode() == "Light" else "#2b2b2b"
        fg_color = "#000000" if ctk.get_appearance_mode() == "Light" else "#ffffff"
        
        style.configure("History.Treeview",
                       background=bg_color,
                       foreground=fg_color,
                       fieldbackground=bg_color,
                       borderwidth=0,
                       rowheight=32)
        style.map('History.Treeview', background=[('selected', th.ACCENT_PRIMARY)])
        
        style.configure("History.Treeview.Heading",
                       background=th.ACCENT_PRIMARY,
                       foreground="white",
                       relief="flat",
                       font=('Arial', 10, 'bold'))
        style.map("History.Treeview.Heading",
                 background=[('active', th.ACCENT_HOVER)])
        
        # Добавляем Customer и Project колонки
        columns = ("datetime", "pdf_name", "customer", "project", "tag_no", "stats")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="History.Treeview"
        )
        
        # Настройка колонок
        self.tree.heading("datetime", text="Date & Time")
        self.tree.heading("pdf_name", text="PDF File")
        self.tree.heading("customer", text="Customer")
        self.tree.heading("project", text="Project")
        self.tree.heading("tag_no", text="TAG No")
        self.tree.heading("stats", text="Statistics")
        
        self.tree.column("datetime", width=150, anchor="w")
        self.tree.column("pdf_name", width=200, anchor="w")
        self.tree.column("customer", width=150, anchor="w")
        self.tree.column("project", width=150, anchor="w")
        self.tree.column("tag_no", width=120, anchor="center")
        self.tree.column("stats", width=180, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(th.SPACING_LG, 0), pady=th.SPACING_LG)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=th.SPACING_LG, padx=(0, th.SPACING_LG))
        
        # Загружаем историю
        self.refresh_history()
    
    def refresh_history(self):
        """Обновляет историю"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Загружаем данные
        history = self.history_manager.get_all()
        
        for record in history:
            datetime_str = record.get("datetime", "")
            pdf_name = record.get("pdf_name", "")
            customer = record.get("customer", "N/A")
            project = record.get("project", "N/A")
            tag_no = record.get("tag_no", "N/A")
            stats = record.get("stats", {})
            
            # Форматируем статистику
            stats_str = f"✅ {stats.get('equal', 0)} | ❌ {stats.get('notEqual', 0)} | 🆕 {stats.get('new', 0)}"
            
            self.tree.insert("", "end", values=(
                datetime_str,
                pdf_name,
                customer,
                project,
                tag_no,
                stats_str
            ))
    
    def clear_history(self):
        """Очищает всю историю"""
        result = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to clear all history?\nThis action cannot be undone."
        )
        
        if result:
            self.history_manager.clear()
            self.refresh_history()
            messagebox.showinfo("Success", "✅ History cleared!")
