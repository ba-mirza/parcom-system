import customtkinter as ctk
from tkinter import filedialog
import os
import theme as th


class FilePicker(ctk.CTkFrame):
    def __init__(self, master, label_text, file_types, is_pinnable=False, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.file_types = file_types
        self.is_pinnable = is_pinnable
        self.filepath = None
        self.is_pinned = False
        self.on_file_selected = None

        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(
            self,
            text=label_text,
            width=100,
            anchor="w",
            text_color=th.TEXT_PRIMARY
        )
        self.label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="No file selected",
            state="readonly",
            fg_color=th.BG_TERTIARY,
            border_color=th.BORDER_DEFAULT
        )
        self.entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.browse_btn = ctk.CTkButton(
            self,
            text="Browse...",
            width=100,
            fg_color=th.ACCENT_PRIMARY,
            hover_color=th.ACCENT_HOVER,
            command=self.browse_file
        )
        self.browse_btn.grid(row=0, column=2, padx=5, pady=10)

        if is_pinnable:
            self.pin_btn = ctk.CTkButton(
                self,
                text="📌 Pin",
                width=80,
                fg_color=("gray70", "gray30"),
                hover_color=("gray60", "gray40"),
                command=self.toggle_pin
            )
            self.pin_btn.grid(row=0, column=3, padx=(5, 10), pady=10)

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title=f"Select {self.label.cget('text')}",
            filetypes=self.file_types
        )

        if filepath:
            self.set_file(filepath)

    def set_file(self, filepath, is_pinned=False):
        if not os.path.exists(filepath):
            return

        self.filepath = filepath
        self.is_pinned = is_pinned

        filename = os.path.basename(filepath)
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, filename)
        self.entry.configure(state="readonly")

        if self.is_pinnable:
            if is_pinned:
                self.pin_btn.configure(text="📌 Pinned", fg_color=th.SUCCESS)
            else:
                self.pin_btn.configure(text="📌 Pin", fg_color=("gray70", "gray30"))

        if self.on_file_selected:
            self.on_file_selected(filepath, is_pinned)

    def toggle_pin(self):
        if not self.filepath:
            return

        self.is_pinned = not self.is_pinned

        if self.is_pinned:
            self.pin_btn.configure(text="📌 Pinned", fg_color=th.SUCCESS)
        else:
            self.pin_btn.configure(text="📌 Pin", fg_color=("gray70", "gray30"))

        if self.on_file_selected:
            self.on_file_selected(self.filepath, self.is_pinned)

    def get_file(self):
        return self.filepath

    def clear(self):
        self.filepath = None
        self.is_pinned = False
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.configure(state="readonly", placeholder_text="No file selected")

        if self.is_pinnable:
            self.pin_btn.configure(text="📌 Pin", fg_color=("gray70", "gray30"))
