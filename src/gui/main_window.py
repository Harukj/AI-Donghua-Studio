import customtkinter as ctk

from gui.sidebar import Sidebar
from gui.dashboard import Dashboard
from gui.statusbar import StatusBar

import config


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(f"{config.APP_NAME} {config.VERSION}")

        self.geometry(
            f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"
        )

        self.minsize(1200, 800)

        ctk.set_appearance_mode(config.THEME)
        ctk.set_default_color_theme(config.COLOR_THEME)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.dashboard = Dashboard(self)
        self.dashboard.grid(row=0, column=1, sticky="nsew")

        self.statusbar = StatusBar(self)
        self.statusbar.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew"
        )