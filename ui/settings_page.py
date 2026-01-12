import customtkinter as ctk
from tkinter import messagebox


class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, config_manager, **kwargs):
        super().__init__(master, **kwargs)

        self.config_manager = config_manager

        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 20), sticky="w")

        api_frame = ctk.CTkFrame(self)
        api_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        api_frame.grid_columnconfigure(1, weight=1)

        api_label = ctk.CTkLabel(
            api_frame,
            text="🌐 API Configuration",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        api_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        endpoint_label = ctk.CTkLabel(api_frame, text="API Endpoint:", anchor="w")
        endpoint_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")

        self.endpoint_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="http://public-api.example.com"
        )
        self.endpoint_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

        current_endpoint = self.config_manager.get_api_endpoint()
        self.endpoint_entry.insert(0, current_endpoint)

        test_btn = ctk.CTkButton(
            api_frame,
            text="🔍 Test Connection",
            command=self.test_connection
        )
        test_btn.grid(row=2, column=0, columnspan=2, padx=15, pady=(5, 15), sticky="ew")

        appearance_frame = ctk.CTkFrame(self)
        appearance_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        appearance_frame.grid_columnconfigure(1, weight=1)

        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="🎨 Appearance",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        appearance_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        theme_label = ctk.CTkLabel(appearance_frame, text="Theme:", anchor="w")
        theme_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")

        self.theme_selector = ctk.CTkComboBox(
            appearance_frame,
            values=["Dark", "Light", "System"],
            state="readonly",
            command=self.change_theme
        )
        self.theme_selector.set(ctk.get_appearance_mode())
        self.theme_selector.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

        about_frame = ctk.CTkFrame(self)
        about_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        about_label = ctk.CTkLabel(
            about_frame,
            text="ℹ️ About",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        about_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        info_text = """PARCOM System Desktop Application
Version: 1.0.0

Features:
- Parse technical drawings (PDF)
- Validate against BOM Excel
- Compare with Order Manager
- Export results to Excel
- Persistent file management
- Parsing history tracking

Developed with today.development using Python & CustomTkinter"""

        info_label = ctk.CTkLabel(
            about_frame,
            text=info_text,
            justify="left",
            font=ctk.CTkFont(size=11)
        )
        info_label.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")

        save_btn = ctk.CTkButton(
            self,
            text="Save Settings",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.save_settings
        )
        save_btn.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

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

        messagebox.showinfo("Success", "✅ Settings saved!")
