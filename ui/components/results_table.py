from tkinter import ttk

import customtkinter as ctk

import theme as th


class ResultsTable(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.data = []
        self.on_status_changed = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header_label = ctk.CTkLabel(
            self, text="Results", font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
        )
        header_label.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")

        table_container = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT,
        )
        table_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            rowheight=32,
            focusthickness=1,
            focuscolor="#cfe2f3",
        )
        style.map(
            "Treeview",
            background=[("selected", "white")],
            foreground=[("selected", "black")],
        )

        style.configure(
            "Treeview.Heading",
            background="#1f6aa5",
            foreground="white",
            relief="flat",
            font=("Arial", 10, "bold"),
        )
        style.map("Treeview.Heading", background=[("active", "#144870")])

        columns = (
            "pos",
            "description",
            "material",
            "bom_material",
            "order_material",
            "quantity",
            "status",
            "note",
        )
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings")

        self.tree.heading("pos", text="Pos")
        self.tree.heading("description", text="Description")
        self.tree.heading("material", text="Material (PDF)")
        self.tree.heading("bom_material", text="Material (BOM)")
        self.tree.heading("order_material", text="Material (Order)")
        self.tree.heading("quantity", text="Qty")
        self.tree.heading("status", text="Status")
        self.tree.heading("note", text="Note")

        self.tree.column("pos", width=60, anchor="center")
        self.tree.column("description", width=180, anchor="center")
        self.tree.column("material", width=200, anchor="center")
        self.tree.column("bom_material", width=200, anchor="center")
        self.tree.column("order_material", width=200, anchor="center")
        self.tree.column("quantity", width=60, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("note", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_container, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<Double-1>", self.on_double_click)

        self.tree.tag_configure("equal", background="#2d5016")
        self.tree.tag_configure("notEqual", background="#5c1a1a")
        self.tree.tag_configure("new", background="#5c4d1a")

    def load_data(self, table2_data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.data = table2_data

        for item in table2_data:
            pos = item.get("pos", "")
            description = item.get("description", "")
            material = item.get("material", "")
            bom_material = item.get("bom_material", "-")
            order_material = item.get("order_material", "-")
            quantity = item.get("quantity", "")
            status = item.get("status", "")
            note = item.get("note", "")

            if not bom_material or bom_material == "":
                bom_material = "-"
            if not order_material or order_material == "":
                order_material = "-"

            tag = status if status in ["equal", "notEqual", "new"] else ""

            self.tree.insert(
                "",
                "end",
                values=(
                    pos,
                    description,
                    material,
                    bom_material,
                    order_material,
                    quantity,
                    status,
                    note,
                ),
                tags=(tag,),
            )

    def on_double_click(self, event):
        item = self.tree.selection()
        if not item:
            return

        values = list(self.tree.item(item[0])["values"])
        current_status = values[6]  # status в колонке 6

        if current_status == "equal":
            new_status = "notEqual"
            new_tag = "notEqual"
        elif current_status == "notEqual":
            new_status = "equal"
            new_tag = "equal"
        else:
            return

        values[6] = new_status
        self.tree.item(item[0], values=values, tags=(new_tag,))

        row_index = self.tree.index(item[0])
        if row_index < len(self.data):
            self.data[row_index]["status"] = new_status

        if self.on_status_changed:
            self.on_status_changed()

    def get_data(self):
        return self.data

    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data = []
