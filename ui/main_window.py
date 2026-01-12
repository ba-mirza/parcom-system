import customtkinter as ctk
from ui.home_page import HomePage
from ui.results_page import ResultsPage
from ui.history_page import HistoryPage
from ui.settings_page import SettingsPage
import theme as th


class MainWindow(ctk.CTk):
    def __init__(self, config_manager, history_manager, api_client):
        super().__init__()

        self.config_manager = config_manager
        self.history_manager = history_manager
        self.api_client = api_client

        self.title("ParCom System")
        self.geometry("1400x900")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=th.BG_SECONDARY
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        # Логотип
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=th.SPACING_LG, pady=(th.SPACING_2XL, th.SPACING_XL), sticky="ew")

        logo_label = ctk.CTkLabel(logo_frame, text="📄", font=ctk.CTkFont(size=32))
        logo_label.pack(pady=(0, th.SPACING_SM))

        app_name = ctk.CTkLabel(
            logo_frame,
            text="ECV PARCOM",
            font=ctk.CTkFont(size=th.FONT_SIZE_XL, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        app_name.pack()

        self.nav_buttons = {}

        nav_items = [
            ("home", "🏠", "Home"),
            ("results", "📊", "Results"),
            ("history", "📋", "History"),
            ("settings", "⚙️", "Settings")
        ]

        for idx, (key, icon, text) in enumerate(nav_items, start=1):
            self.nav_buttons[key] = self.create_nav_button(
                self.sidebar, icon, text, key, idx
            )

        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=th.BORDER_DEFAULT
        )
        divider.grid(row=5, column=0, padx=th.SPACING_LG, pady=th.SPACING_XL, sticky="ew")

        docx_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        docx_frame.grid(row=6, column=0, padx=th.SPACING_LG, pady=(th.SPACING_MD, th.SPACING_SM), sticky="nw")

        ctk.CTkLabel(
            docx_frame,
            text="📄 DOCX Templates",
            font=ctk.CTkFont(size=th.FONT_SIZE_SM),
            text_color=th.TEXT_MUTED
        ).pack(anchor="w")

        ctk.CTkLabel(
            docx_frame,
            text="Coming Soon",
            font=ctk.CTkFont(size=th.FONT_SIZE_SM - 1),
            text_color=th.TEXT_MUTED
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(size=th.FONT_SIZE_SM),
            text_color=th.TEXT_MUTED
        ).grid(row=7, column=0, padx=th.SPACING_LG, pady=(th.SPACING_MD, th.SPACING_LG), sticky="s")

        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.pages = {}

        self.pages["home"] = HomePage(
            self.content_frame,
            config_manager=self.config_manager,
            history_manager=self.history_manager,
            api_client=self.api_client,
            on_parse_complete=self.on_parse_complete
        )

        self.pages["results"] = ResultsPage(
            self.content_frame,
            api_client=self.api_client
        )

        self.pages["history"] = HistoryPage(
            self.content_frame,
            history_manager=self.history_manager
        )

        self.pages["settings"] = SettingsPage(
            self.content_frame,
            config_manager=self.config_manager
        )

        self.current_page = None
        self.select_page("home")

    def create_nav_button(self, parent, icon, text, key, row):
        btn = ctk.CTkButton(
            parent,
            text=f"{icon}  {text}",
            font=ctk.CTkFont(size=th.FONT_SIZE_BASE),
            height=40,
            corner_radius=th.RADIUS_MD,
            fg_color="transparent",
            text_color=th.TEXT_SECONDARY,
            hover_color=th.BG_HOVER,
            anchor="w",
            command=lambda: self.select_page(key)
        )
        btn.grid(row=row, column=0, padx=th.SPACING_LG, pady=th.SPACING_XS, sticky="ew")
        return btn

    def select_page(self, page_name):
        if self.current_page:
            self.pages[self.current_page].grid_forget()

        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        self.current_page = page_name

        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(
                    fg_color=th.BG_TERTIARY,
                    text_color=th.TEXT_PRIMARY
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=th.TEXT_SECONDARY
                )

        if page_name == "history":
            self.pages["history"].refresh_history()

    def on_parse_complete(self, result):
        self.pages["results"].load_results(result)
        self.select_page("results")
