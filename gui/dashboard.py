import customtkinter as ctk


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="Welcome to AI Donghua Studio",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=40)

        info = """
Project :
Toàn Dân Tạo Mộng

Characters : 0

Episodes : 0

Scenes : 0

Videos : 0
"""

        label = ctk.CTkLabel(
            self,
            text=info,
            justify="left",
            font=("Arial", 20)
        )

        label.pack()