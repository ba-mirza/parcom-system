import customtkinter as ctk
from utils.config_manager import ConfigManager
from utils.history_manager import HistoryManager
from api.client import APIClient
from ui.main_window import MainWindow
import theme as th


def main():
    config_manager = ConfigManager()
    history_manager = HistoryManager()

    api_endpoint = config_manager.get_api_endpoint()
    api_client = APIClient(api_endpoint)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = MainWindow(config_manager, history_manager, api_client)

    app.mainloop()


if __name__ == "__main__":
    main()
