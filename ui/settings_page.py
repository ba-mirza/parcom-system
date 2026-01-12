import customtkinter as ctk
from tkinter import messagebox
import theme as th


class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, config_manager, api_client, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.config_manager = config_manager
        self.api_client = api_client

        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=th.FONT_SIZE_2XL, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        title_label.grid(row=0, column=0, padx=th.SPACING_2XL, pady=(th.SPACING_2XL, th.SPACING_XL), sticky="w")

        api_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT
        )
        api_frame.grid(row=1, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_LG), sticky="ew")
        api_frame.grid_columnconfigure(1, weight=1)

        api_label = ctk.CTkLabel(
            api_frame,
            text="API Configuration",
            font=ctk.CTkFont(size=th.FONT_SIZE_LG, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        api_label.grid(row=0, column=0, columnspan=2, padx=th.SPACING_LG, pady=(th.SPACING_LG, th.SPACING_MD), sticky="w")

        endpoint_label = ctk.CTkLabel(
            api_frame,
            text="API Endpoint:",
            anchor="w",
            text_color=th.TEXT_PRIMARY
        )
        endpoint_label.grid(row=1, column=0, padx=th.SPACING_LG, pady=th.SPACING_MD, sticky="w")

        self.endpoint_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="http://localhost:8000",
            fg_color=th.BG_TERTIARY,
            border_color=th.BORDER_DEFAULT
        )
        self.endpoint_entry.grid(row=1, column=1, padx=th.SPACING_LG, pady=th.SPACING_MD, sticky="ew")

        current_endpoint = self.config_manager.get_api_endpoint()
        self.endpoint_entry.insert(0, current_endpoint)

        test_btn = ctk.CTkButton(
            api_frame,
            text="Test Connection",
            fg_color=th.ACCENT_PRIMARY,
            hover_color=th.ACCENT_HOVER,
            command=self.test_connection
        )
        test_btn.grid(row=2, column=0, columnspan=2, padx=th.SPACING_LG, pady=(th.SPACING_SM, th.SPACING_LG), sticky="ew")

        appearance_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT
        )
        appearance_frame.grid(row=2, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_LG), sticky="ew")
        appearance_frame.grid_columnconfigure(1, weight=1)

        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=ctk.CTkFont(size=th.FONT_SIZE_LG, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        appearance_label.grid(row=0, column=0, columnspan=2, padx=th.SPACING_LG, pady=(th.SPACING_LG, th.SPACING_MD), sticky="w")

        theme_label = ctk.CTkLabel(
            appearance_frame,
            text="Theme:",
            anchor="w",
            text_color=th.TEXT_PRIMARY
        )
        theme_label.grid(row=1, column=0, padx=th.SPACING_LG, pady=th.SPACING_MD, sticky="w")

        self.theme_selector = ctk.CTkComboBox(
            appearance_frame,
            values=["Dark", "Light", "System"],
            state="readonly",
            fg_color=th.BG_TERTIARY,
            border_color=th.BORDER_DEFAULT,
            button_color=th.ACCENT_PRIMARY,
            button_hover_color=th.ACCENT_HOVER,
            command=self.change_theme
        )
        self.theme_selector.set(ctk.get_appearance_mode())
        self.theme_selector.grid(row=1, column=1, padx=th.SPACING_LG, pady=th.SPACING_MD, sticky="ew")

        about_frame = ctk.CTkFrame(
            self,
            corner_radius=th.RADIUS_LG,
            fg_color=th.BG_SECONDARY,
            border_width=1,
            border_color=th.BORDER_DEFAULT
        )
        about_frame.grid(row=3, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_LG), sticky="ew")

        about_label = ctk.CTkLabel(
            about_frame,
            text="ℹ️ About",
            font=ctk.CTkFont(size=th.FONT_SIZE_LG, weight="bold"),
            text_color=th.TEXT_PRIMARY
        )
        about_label.grid(row=0, column=0, padx=th.SPACING_LG, pady=(th.SPACING_LG, th.SPACING_SM), sticky="w")

        info_text = """ParCom System Desktop Application
Version: 1.0.2

Features:
- Parse technical drawings (PDF)
- Validate against BOM Excel
- Compare with Order Manager
- Export results to Excel
- Persistent file management
- Parsing history tracking
"""

        info_label = ctk.CTkLabel(
            about_frame,
            text=info_text,
            justify="left",
            font=ctk.CTkFont(size=th.FONT_SIZE_SM),
            text_color=th.TEXT_SECONDARY
        )
        info_label.grid(row=1, column=0, padx=th.SPACING_LG, pady=(th.SPACING_SM, th.SPACING_LG), sticky="w")

        save_btn = ctk.CTkButton(
            self,
            text="Save Settings",
            height=45,
            corner_radius=th.RADIUS_MD,
            font=ctk.CTkFont(size=th.FONT_SIZE_BASE, weight="bold"),
            fg_color=th.ACCENT_PRIMARY,
            hover_color=th.ACCENT_HOVER,
            command=self.save_settings
        )
        save_btn.grid(row=4, column=0, padx=th.SPACING_2XL, pady=(0, th.SPACING_2XL), sticky="ew")

    def test_connection(self):
        endpoint = self.endpoint_entry.get().strip()

        if not endpoint:
            messagebox.showerror("Error", "Please enter API endpoint!")
            return

        try:
            import requests
            response = requests.get(f"{endpoint}/", timeout=5)

            if response.status_code == 200:
                data = response.json()
                messagebox.showinfo(
                    "Success",
                    f"✅ Connection successful!\n\n{data.get('message', 'API is online')}"
                )
            else:
                messagebox.showerror("Error", f"❌ Server returned status {response.status_code}")

        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Error",
                "❌ Connection failed!\n\nMake sure the API server is running."
            )
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error: {str(e)}")

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

    def save_settings(self):
        endpoint = self.endpoint_entry.get().strip()

        if not endpoint:
            messagebox.showerror("Error", "API endpoint cannot be empty!")
            return

        self.config_manager.set_api_endpoint(endpoint)

        self.api_client.update_endpoint(endpoint)

        messagebox.showinfo("Success", "Settings saved!\n\nAPI endpoint updated successfully.")
