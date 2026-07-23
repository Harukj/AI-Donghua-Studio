import customtkinter as ctk

class NovelWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		self.label = ctk.CTkLabel(
			self, 
			text="Novel Import System (Sprint 4)\nHệ thống nạp tệp truyện và phân tách chương tự động đang được thiết lập...",
			font=ctk.CTkFont(size=16, weight="bold")
		)
		self.label.pack(expand=True)
