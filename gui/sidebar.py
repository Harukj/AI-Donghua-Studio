import customtkinter as ctk

import config

MENU = [
    "🏠 Dashboard",
    "📁 Projects",
    "📖 Novel",
    "🎭 Characters",
    "🌍 Environment",
    "📷 Cameras",
    "🎬 Motions",
    "📝 Storyboard",
    "✨ LTX Prompt",
    "🎥 LTX Studio",
    "📦 Export",
    "⚙ Settings",
]


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            width=config.SIDEBAR_WIDTH,
            corner_radius=0
        )

        self.grid_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="AI Donghua Studio",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)

        for item in MENU:

            button = ctk.CTkButton(
                self,
                text=item,
                height=42
            )

            button.pack(
                padx=10,
                pady=5,
                fill="x"
            )