import customtkinter as ctk


class StatusBar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, height=28)

        label = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w"
        )

        label.pack(
            padx=10,
            fill="x"
        )