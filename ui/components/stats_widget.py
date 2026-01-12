import customtkinter as ctk
import theme as th


class StatsWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT,
            **kwargs
        )

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Statistics",
            font=ctk.CTkFont(size=th.FONT_SIZE_LG, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        self.title_label.grid(row=0, column=0, columnspan=4, padx=th.SPACING_LG, pady=(th.SPACING_LG, th.SPACING_SM), sticky="w")

        self.total_label = self._create_metric("Total", "0", 1, 0, th.TEXT_PRIMARY)
        self.equal_label = self._create_metric("Equal", "0", 1, 1, th.SUCCESS)
        self.not_equal_label = self._create_metric("Not Equal", "0", 1, 2, th.ERROR)
        self.new_label = self._create_metric("New", "0", 1, 3, th.WARNING)

    def _create_metric(self, label_text, value_text, row, col, color):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=row, column=col, padx=th.SPACING_LG, pady=th.SPACING_MD, sticky="ew")

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=th.FONT_SIZE_SM),
            text_color=th.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(side="top", anchor="w")

        value = ctk.CTkLabel(
            frame,
            text=value_text,
            font=ctk.CTkFont(size=th.FONT_SIZE_2XL, weight="bold"),
            text_color=color
        )
        value.pack(side="top", anchor="w", pady=(th.SPACING_XS, 0))

        return value

    def update_stats(self, total=0, equal=0, not_equal=0, new=0):
        self.total_label.configure(text=str(total))
        self.equal_label.configure(text=str(equal))
        self.not_equal_label.configure(text=str(not_equal))
        self.new_label.configure(text=str(new))

    def clear(self):
        self.update_stats(0, 0, 0, 0)
