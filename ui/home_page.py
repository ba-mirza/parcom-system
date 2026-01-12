import customtkinter as ctk
from tkinter import messagebox
import os
import threading
from ui.components.file_picker import FilePicker
import theme as th


class HomePage(ctk.CTkFrame):
    def __init__(self, master, config_manager, history_manager, api_client, on_parse_complete=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.config_manager = config_manager
        self.history_manager = history_manager
        self.api_client = api_client
        self.on_parse_complete = on_parse_complete

        self.current_result = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.files_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT
        )
        self.files_frame.grid(row=0, column=0, padx=th.SPACING_2XL, pady=th.SPACING_2XL, sticky="ew")
        self.files_frame.grid_columnconfigure(0, weight=1)

        files_label = ctk.CTkLabel(
            self.files_frame,
            text="📁 File Upload",
            font=ctk.CTkFont(size=th.FONT_SIZE_LG, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        files_label.grid(row=0, column=0, padx=th.SPACING_LG, pady=(th.SPACING_LG, th.SPACING_MD), sticky="w")

        self.pdf_picker = FilePicker(
            self.files_frame,
            label_text="PDF:",
            file_types=[("PDF files", "*.pdf")],
            is_pinnable=False
        )
        self.pdf_picker.grid(row=1, column=0, padx=th.SPACING_LG, pady=th.SPACING_SM, sticky="ew")

        self.bom_picker = FilePicker(
            self.files_frame,
            label_text="BOM Excel:",
            file_types=[("Excel files", "*.xlsx *.xls")],
            is_pinnable=True
        )
        self.bom_picker.grid(row=2, column=0, padx=th.SPACING_LG, pady=th.SPACING_SM, sticky="ew")
        self.bom_picker.on_file_selected = self.on_bom_file_selected

        self.manager_picker = FilePicker(
            self.files_frame,
            label_text="Manager Excel:",
            file_types=[("Excel files", "*.xlsx *.xls")],
            is_pinnable=True
        )
        self.manager_picker.grid(row=3, column=0, padx=th.SPACING_LG, pady=th.SPACING_SM, sticky="ew")
        self.manager_picker.on_file_selected = self.on_manager_file_selected

        sheet_frame = ctk.CTkFrame(self.files_frame, fg_color="transparent")
        sheet_frame.grid(row=4, column=0, padx=th.SPACING_LG, pady=th.SPACING_SM, sticky="ew")

        sheet_label = ctk.CTkLabel(
            sheet_frame,
            text="BOM Sheet:",
            width=100,
            anchor="w",
            text_color=th.TEXT_PRIMARY
        )
        sheet_label.pack(side="left", padx=(0, th.SPACING_SM))

        self.sheet_selector = ctk.CTkComboBox(
            sheet_frame,
            values=[f"Foglio {i}" for i in range(1, 15)],
            width=150,
            state="readonly",
            fg_color=th.BG_TERTIARY,
            border_color=th.BORDER_DEFAULT,
            button_color=th.ACCENT_PRIMARY,
            button_hover_color=th.ACCENT_HOVER
        )
        self.sheet_selector.set("Foglio 1")
        self.sheet_selector.pack(side="left", padx=th.SPACING_SM)

        self.parse_btn = ctk.CTkButton(
            self.files_frame,
            text="Parse Documents",
            height=45,
            corner_radius=th.RADIUS_MD,
            font=ctk.CTkFont(size=th.FONT_SIZE_BASE, weight="bold"),
            fg_color=th.ACCENT_PRIMARY,
            hover_color=th.ACCENT_HOVER,
            command=self.start_parsing
        )
        self.parse_btn.grid(row=5, column=0, padx=th.SPACING_LG, pady=(th.SPACING_LG, th.SPACING_LG), sticky="ew")

        self.progress = ctk.CTkProgressBar(
            self.files_frame,
            progress_color=th.ACCENT_PRIMARY
        )
        self.progress.grid(row=6, column=0, padx=th.SPACING_LG, pady=(0, th.SPACING_LG), sticky="ew")
        self.progress.set(0)
        self.progress.grid_remove()

        info_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT
        )
        info_frame.grid(row=1, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_2XL), sticky="nsew")
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_rowconfigure(1, weight=1)

        info_title = ctk.CTkLabel(
            info_frame,
            text="ℹ️ How it works",
            font=ctk.CTkFont(size=th.FONT_SIZE_LG, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        info_title.grid(row=0, column=0, padx=th.SPACING_LG, pady=(th.SPACING_LG, th.SPACING_SM), sticky="w")

        info_text = """1️⃣  Select PDF drawing file (required)
2️⃣  BOM and Manager Excel files are pinned automatically
3️⃣  Choose the correct BOM sheet (Foglio 1-14)
4️⃣  Click "Parse Documents" to start processing
5️⃣  View results in the Results page
6️⃣  Export to Excel with custom column selection

💡 Tip: Pin your BOM and Manager files once - they'll stay for future use!"""

        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=th.FONT_SIZE_SM),
            text_color=th.TEXT_SECONDARY,
            justify="left",
            anchor="w"
        )
        info_label.grid(row=1, column=0, padx=th.SPACING_LG, pady=(th.SPACING_SM, th.SPACING_LG), sticky="nw")

        self.load_pinned_files()

    def load_pinned_files(self):
        bom_path = self.config_manager.get_pinned_file("bom_excel")
        if bom_path and os.path.exists(bom_path):
            self.bom_picker.set_file(bom_path, is_pinned=True)

        manager_path = self.config_manager.get_pinned_file("manager_excel")
        if manager_path and os.path.exists(manager_path):
            self.manager_picker.set_file(manager_path, is_pinned=True)

        last_sheet = self.config_manager.get("last_bom_sheet_index", 0)
        self.sheet_selector.set(f"Foglio {last_sheet + 1}")

    def on_bom_file_selected(self, filepath, is_pinned):
        if is_pinned:
            self.config_manager.set_pinned_file("bom_excel", filepath)
        else:
            self.config_manager.set_pinned_file("bom_excel", None)

    def on_manager_file_selected(self, filepath, is_pinned):
        if is_pinned:
            self.config_manager.set_pinned_file("manager_excel", filepath)
        else:
            self.config_manager.set_pinned_file("manager_excel", None)

    def start_parsing(self):
        pdf_path = self.pdf_picker.get_file()
        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file!")
            return

        bom_path = self.bom_picker.get_file()
        manager_path = self.manager_picker.get_file()

        sheet_text = self.sheet_selector.get()
        sheet_index = int(sheet_text.split()[1]) - 1

        self.config_manager.set("last_bom_sheet_index", sheet_index)

        self.parse_btn.configure(state="disabled", text="⏳ Parsing...")
        self.progress.grid()
        self.progress.set(0)

        thread = threading.Thread(
            target=self.parse_documents,
            args=(pdf_path, bom_path, manager_path, sheet_index)
        )
        thread.daemon = True
        thread.start()

    def parse_documents(self, pdf_path, bom_path, manager_path, sheet_index):
        try:
            self.animate_progress()

            result = self.api_client.parse_pdf(
                pdf_path=pdf_path,
                bom_path=bom_path,
                manager_path=manager_path,
                bom_sheet_index=sheet_index
            )

            self.after(0, lambda: self.on_parsing_complete(result, pdf_path))

        except Exception as e:
            self.after(0, lambda: self.on_parse_error(str(e)))

    def animate_progress(self):
        for i in range(10):
            if not self.parse_btn.cget("state") == "disabled":
                break
            self.after(i * 100, lambda v=i/10: self.progress.set(v))

    def on_parsing_complete(self, result, pdf_path):
        self.progress.set(1.0)
        self.parse_btn.configure(state="normal", text="🚀 Parse Documents")
        self.progress.grid_remove()

        if not result.get("success"):
            messagebox.showerror("Error", result.get("error", "Unknown error"))
            return

        self.current_result = result

        table2 = result.get("data", {}).get("table2", [])
        table3 = result.get("data", {}).get("table3", [])
        tag_no = next((item.get("TAG No") for item in table3 if "TAG No" in item), None)
        pdf_name = os.path.basename(pdf_path)

        stats = self.calculate_stats(table2)
        self.history_manager.add_record(pdf_name, tag_no, stats)

        if self.on_parse_complete:
            self.on_parse_complete(result)

        messagebox.showinfo("Success", f"✅ Parsing completed!\n\nTotal components: {len(table2)}\n\nSwitching to Results page...")

    def on_parse_error(self, error):
        self.progress.grid_remove()
        self.parse_btn.configure(state="normal", text="🚀 Parse Documents")
        messagebox.showerror("Error", f"Parsing failed:\n{error}")

    def calculate_stats(self, table2):
        total = len(table2)
        equal = len([item for item in table2 if item.get("status") == "equal"])
        not_equal = len([item for item in table2 if item.get("status") == "notEqual"])
        new = len([item for item in table2 if item.get("status") == "new"])

        return {
            "total": total,
            "equal": equal,
            "notEqual": not_equal,
            "new": new
        }
