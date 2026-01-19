"""
Страница результатов парсинга - полноэкранная таблица
"""

import threading
from tkinter import filedialog, messagebox

import customtkinter as ctk

import theme as th
from ui.components.results_table import ResultsTable
from ui.components.stats_widget import StatsWidget


class ResultsPage(ctk.CTkFrame):
    def __init__(self, master, api_client, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.api_client = api_client
        self.current_result = None

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)  # Таблица теперь row 3

        # ===== HEADER =====
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(
            row=0,
            column=0,
            padx=th.SPACING_2XL,
            pady=(th.SPACING_2XL, th.SPACING_MD),
            sticky="ew",
        )
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Parsing Results",
            font=ctk.CTkFont(size=th.FONT_SIZE_2XL, weight="bold"),
            text_color=th.TEXT_PRIMARY,
        )
        title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            header_frame,
            text="No results yet. Parse a document first.",
            font=ctk.CTkFont(size=th.FONT_SIZE_SM),
            text_color=th.TEXT_SECONDARY,
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(th.SPACING_XS, 0))

        # ===== INFO CARD (Customer/Project) =====
        self.info_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT,
        )
        self.info_frame.grid(
            row=1, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_MD), sticky="ew"
        )
        self.info_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Заголовок карточки
        info_title = ctk.CTkLabel(
            self.info_frame,
            text="📋 Document Information",
            font=ctk.CTkFont(size=th.FONT_SIZE_BASE, weight="bold"),
            text_color=th.TEXT_PRIMARY,
        )
        info_title.grid(
            row=0,
            column=0,
            columnspan=3,
            padx=th.SPACING_LG,
            pady=(th.SPACING_LG, th.SPACING_SM),
            sticky="w",
        )

        # Поля информации
        self.info_labels = {}
        info_fields = [
            ("customer", "Customer"),
            ("project", "Project/Location"),
            ("tag_no", "TAG No"),
            ("po_no", "P.O. No"),
            ("epc_user", "EPC/End User"),
            ("ecv_job", "ECV JOB No"),
        ]

        row_idx = 1
        col_idx = 0

        for key, label_text in info_fields:
            field_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
            field_frame.grid(
                row=row_idx,
                column=col_idx,
                padx=th.SPACING_LG,
                pady=th.SPACING_XS,
                sticky="w",
            )

            label = ctk.CTkLabel(
                field_frame,
                text=f"{label_text}:",
                font=ctk.CTkFont(size=th.FONT_SIZE_SM),
                text_color=th.TEXT_SECONDARY,
            )
            label.pack(anchor="w")

            value = ctk.CTkLabel(
                field_frame,
                text="-",
                font=ctk.CTkFont(size=th.FONT_SIZE_BASE, weight="bold"),
                text_color=th.TEXT_PRIMARY,
            )
            value.pack(anchor="w")

            self.info_labels[key] = value

            col_idx += 1
            if col_idx > 2:
                col_idx = 0
                row_idx += 1

        # Скрываем карточку по умолчанию
        self.info_frame.grid_remove()

        # ===== СТАТИСТИКА =====
        self.stats_widget = StatsWidget(self)
        self.stats_widget.grid(
            row=2, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_MD), sticky="ew"
        )

        # ===== РЕЗУЛЬТАТЫ (ПОЛНОЭКРАННАЯ ТАБЛИЦА) =====
        self.results_table = ResultsTable(self)
        self.results_table.grid(
            row=3, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_MD), sticky="nsew"
        )
        self.results_table.on_status_changed = self.on_status_changed

        # ===== ЭКСПОРТ =====
        export_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT,
        )
        export_frame.grid(
            row=4, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_2XL), sticky="ew"
        )
        export_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Checkboxes для выбора колонок
        columns_label = ctk.CTkLabel(
            export_frame,
            text="Export columns:",
            font=ctk.CTkFont(size=th.FONT_SIZE_BASE, weight="bold"),
            text_color=th.TEXT_PRIMARY,
        )
        columns_label.grid(
            row=0,
            column=0,
            columnspan=3,
            padx=th.SPACING_LG,
            pady=(th.SPACING_LG, th.SPACING_SM),
            sticky="w",
        )

        self.export_columns = {
            "pos": ctk.CTkCheckBox(
                export_frame,
                text="Pos",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
            "description": ctk.CTkCheckBox(
                export_frame,
                text="Description",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
            "material": ctk.CTkCheckBox(
                export_frame,
                text="Material (PDF)",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
            "bom_material": ctk.CTkCheckBox(
                export_frame,
                text="Material (BOM)",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
            "order_material": ctk.CTkCheckBox(
                export_frame,
                text="Material (Order)",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
            "quantity": ctk.CTkCheckBox(
                export_frame,
                text="Quantity",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
            "manager_quantity": ctk.CTkCheckBox(
                export_frame,
                text="Manager Qty",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
            "note": ctk.CTkCheckBox(
                export_frame,
                text="Note",
                text_color=th.TEXT_SECONDARY,
                fg_color=th.ACCENT_PRIMARY,
                hover_color=th.ACCENT_HOVER,
            ),
        }

        # По умолчанию выбраны: pos, description, material, quantity, note
        default_selected = ["pos", "description", "material", "quantity", "note"]

        for i, (key, checkbox) in enumerate(self.export_columns.items()):
            if key in default_selected:
                checkbox.select()

            row = 1 + i // 3
            col = i % 3
            checkbox.grid(
                row=row, column=col, padx=th.SPACING_LG, pady=th.SPACING_XS, sticky="w"
            )

        # Export Button
        self.export_btn = ctk.CTkButton(
            export_frame,
            text="💾 Export to Excel",
            height=45,
            corner_radius=th.RADIUS_MD,
            font=ctk.CTkFont(size=th.FONT_SIZE_BASE, weight="bold"),
            fg_color=th.ACCENT_PRIMARY,
            hover_color=th.ACCENT_HOVER,
            state="disabled",
            command=self.export_to_excel,
        )
        self.export_btn.grid(
            row=4,
            column=0,
            columnspan=3,
            padx=th.SPACING_LG,
            pady=th.SPACING_LG,
            sticky="ew",
        )

    def load_results(self, result):
        """Загружает результаты парсинга"""
        self.current_result = result

        # Извлекаем table3
        table3 = result.get("data", {}).get("table3", [])

        # Создаем словарь для быстрого доступа
        info_dict = {}
        for item in table3:
            for key, value in item.items():
                info_dict[key] = value

        # Обновляем subtitle и info card
        tag_no = info_dict.get("TAG No", "Unknown")
        self.subtitle_label.configure(text=f"TAG No: {tag_no}")

        # Показываем и заполняем info card
        self.info_frame.grid()
        self.info_labels["customer"].configure(text=info_dict.get("CUSTOMER", "-"))
        self.info_labels["project"].configure(
            text=info_dict.get("PROJECT/LOCATION", "-")
        )
        self.info_labels["tag_no"].configure(text=info_dict.get("TAG No", "-"))
        self.info_labels["po_no"].configure(text=info_dict.get("P.O. No", "-"))
        self.info_labels["epc_user"].configure(text=info_dict.get("EPC/END USER", "-"))
        self.info_labels["ecv_job"].configure(text=info_dict.get("ECV JOB No", "-"))

        # Загружаем данные таблицы
        table2 = result.get("data", {}).get("table2", [])
        self.results_table.load_data(table2)

        # Обновляем статистику
        self.update_statistics(table2)

        # Активируем кнопку экспорта
        self.export_btn.configure(state="normal")

    def update_statistics(self, table2):
        """Обновляет статистику"""
        stats = self.calculate_stats(table2)
        self.stats_widget.update_stats(
            total=stats["total"],
            equal=stats["equal"],
            not_equal=stats["notEqual"],
            new=stats["new"],
        )

    def calculate_stats(self, table2):
        """Вычисляет статистику"""
        total = len(table2)
        equal = len([item for item in table2 if item.get("status") == "equal"])
        not_equal = len([item for item in table2 if item.get("status") == "notEqual"])
        new = len([item for item in table2 if item.get("status") == "new"])

        return {"total": total, "equal": equal, "notEqual": not_equal, "new": new}

    def on_status_changed(self):
        """Вызывается при изменении статуса в таблице"""
        updated_data = self.results_table.get_data()
        self.update_statistics(updated_data)

        if self.current_result:
            self.current_result["data"]["table2"] = updated_data

    def export_to_excel(self):
        """Экспортирует результаты в Excel"""
        if not self.current_result:
            return

        # Получаем выбранные колонки
        selected_columns = [
            key for key, checkbox in self.export_columns.items() if checkbox.get() == 1
        ]

        # Фильтруем данные
        filtered_data = self.filter_export_data(
            self.current_result["data"]["table2"], selected_columns
        )

        # Обновляем данные в результате
        export_result = self.current_result.copy()
        export_result["data"]["table2"] = filtered_data

        # Выбираем путь сохранения
        filepath = filedialog.asksaveasfilename(
            title="Save Excel file",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
        )

        if not filepath:
            return

        # Экспортируем
        self.export_btn.configure(state="disabled", text="⏳ Exporting...")

        thread = threading.Thread(target=self.do_export, args=(export_result, filepath))
        thread.daemon = True
        thread.start()

    def filter_export_data(self, table2, selected_columns):
        """Фильтрует данные для экспорта"""
        filtered = []

        for item in table2:
            filtered_item = {}

            # Всегда включаем status (нужен для цветов)
            if "status" in item:
                filtered_item["status"] = item["status"]

            # Добавляем выбранные колонки
            for col in selected_columns:
                if col in item:
                    filtered_item[col] = item[col]

            filtered.append(filtered_item)

        return filtered

    def do_export(self, result, filepath):
        """Выполняет экспорт (в отдельном потоке)"""
        try:
            success = self.api_client.export_excel(result, filepath)

            if success:
                self.after(0, lambda: self.on_export_complete(filepath))
            else:
                self.after(0, lambda: self.on_export_error("Export failed"))

        except Exception as e:
            self.after(0, lambda: self.on_export_error(str(e)))

    def on_export_complete(self, filepath):
        """Обработка завершения экспорта"""
        self.export_btn.configure(state="normal", text="💾 Export to Excel")
        messagebox.showinfo("Success", f"✅ Excel file saved:\n{filepath}")

    def on_export_error(self, error):
        """Обработка ошибки экспорта"""
        self.export_btn.configure(state="normal", text="💾 Export to Excel")
        messagebox.showerror("Error", f"Export failed:\n{error}")
