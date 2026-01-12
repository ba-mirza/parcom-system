import customtkinter as ctk
from tkinter import ttk, messagebox


class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, history_manager, **kwargs):
        super().__init__(master, **kwargs)

        self.history_manager = history_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="📋 Parsing History",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=10, sticky="w")

        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=10, sticky="e")

        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            width=100,
            command=self.refresh_history
        )
        refresh_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear All",
            width=100,
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self.clear_history
        )
        clear_btn.pack(side="left", padx=5)

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('default')

        style.configure("History.Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       rowheight=30)
        style.map('History.Treeview', background=[('selected', '#1f6aa5')])

        style.configure("History.Treeview.Heading",
                       background="#1f6aa5",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 10, 'bold'))
        style.map("History.Treeview.Heading",
                 background=[('active', '#144870')])

        columns = ("datetime", "pdf_name", "tag_no", "stats")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="History.Treeview"
        )

        self.tree.heading("datetime", text="Date & Time")
        self.tree.heading("pdf_name", text="PDF File")
        self.tree.heading("tag_no", text="TAG No")
        self.tree.heading("stats", text="Statistics")

        self.tree.column("datetime", width=180, anchor="w")
        self.tree.column("pdf_name", width=250, anchor="w")
        self.tree.column("tag_no", width=120, anchor="center")
        self.tree.column("stats", width=200, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 10))

        self.refresh_history()

    def refresh_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = self.history_manager.get_all()

        for record in history:
            datetime_str = record.get("datetime", "")
            pdf_name = record.get("pdf_name", "")
            tag_no = record.get("tag_no", "N/A")
            stats = record.get("stats", {})

            stats_str = f"✅ {stats.get('equal', 0)} | ❌ {stats.get('notEqual', 0)} | 🆕 {stats.get('new', 0)}"

            self.tree.insert("", "end", values=(datetime_str, pdf_name, tag_no, stats_str))

    def clear_history(self):
        result = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to clear all history?\nThis action cannot be undone."
        )

        if result:
            self.history_manager.clear()
            self.refresh_history()
            messagebox.showinfo("Success", "✅ History cleared!")
