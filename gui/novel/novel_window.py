import customtkinter as ctk
from tkinter import messagebox

class NovelWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Thiết lập bố cục lưới (Cột 0: Danh sách tiểu thuyết, Cột 1: Vùng hiển thị chương/nội dung)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=2)
		self.grid_rowconfigure(0, weight=1)
		
		self.selected_novel = None
		
		# 1. PHÂN VÙNG BÊN TRÁI: DANH SÁCH TRUYỆN CHỮ (NOVEL LIBRARY)
		self.left_frame = ctk.CTkFrame(self)
		self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		
		self.title_label = ctk.CTkLabel(
			self.left_frame, text="Novel Library", font=ctk.CTkFont(size=18, weight="bold")
		)
		self.title_label.pack(padx=15, pady=15, anchor="w")
		
		# Nút bấm nạp file truyện mới lên hệ thống (Sẽ liên kết với novel_form ở bước sau)
		self.btn_import_novel = ctk.CTkButton(
			self.left_frame, text="+ Import Novel File", fg_color="#1F6AA5",
			font=ctk.CTkFont(size=13, weight="bold"), command=self.open_import_dialog
		)
		self.btn_import_novel.pack(padx=15, pady=5, fill="x")
		
		self.separator = ctk.CTkLabel(self.left_frame, text="----------------------------------------", text_color="gray")
		self.separator.pack(padx=15, pady=5)
		
		# Khung cuộn chứa danh sách các tác phẩm truyện chữ đã nạp
		self.list_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
		self.list_frame.pack(padx=10, pady=5, fill="both", expand=True)
		
		# 2. PHÂN VÙNG BÊN PHẢI: KHU VỰC CHI TIẾT TÁC PHẨM VÀ PHÂN CHƯƠNG (WORKSPACE)
		self.right_frame = ctk.CTkFrame(self)
		self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
		
		self.workspace_title = ctk.CTkLabel(
			self.right_frame, text="Workspace - Trình xử lý văn bản", font=ctk.CTkFont(size=18, weight="bold")
		)
		self.workspace_title.pack(padx=20, pady=15, anchor="w")
		
		# Khung hiển thị nội dung/chương tạm thời
		self.content_label = ctk.CTkLabel(
			self.right_frame, 
			text="Vui lòng nhấn '+ Import Novel File' để nạp tệp kịch bản truyện chữ\nhoặc chọn một tác phẩm từ danh sách bên trái.",
			font=ctk.CTkFont(size=14, italic=True)
		)
		self.content_label.pack(expand=True)
		
		# Nạp thử danh sách dữ liệu mẫu ban đầu để kiểm tra giao diện
		self.mock_novels = ["Toàn Dân Tạo Mộng - Quyển 1", "Đấu Phá Thương Khung", "Phàm Nhân Tu Tiên"]
		self.refresh_novel_list()

	def refresh_novel_list(self):
		"""Vẽ danh sách các bộ truyện lên màn hình lề trái"""
		for widget in self.list_frame.winfo_children():
			widget.destroy()
			
		for novel_name in self.mock_novels:
			btn = ctk.CTkButton(
				self.list_frame, text=novel_name, anchor="w", height=38,
				fg_color="transparent", text_color=("#000000", "#FFFFFF"),
				command=lambda n=novel_name: self.view_novel_workspace(n)
			)
			btn.pack(fill="x", pady=2, padx=5)

	def view_novel_workspace(self, name):
		"""Hành động khi click chọn vào một bộ truyện chữ"""
		self.selected_novel = name
		self.workspace_title.configure(text=f"Tác phẩm: {name}")
		self.content_label.configure(
			text=f"Hệ thống đang tải các chương và đoạn kịch bản của bộ truyện:\n[{name}]\n\nSẵn sàng để chuyển sang cho Đạo diễn AI bóc tách thực thể phân cảnh.",
			font=ctk.CTkFont(size=14, weight="medium")
		)

	def open_import_dialog(self):
		"""Hộp thoại nạp nhanh tệp tiểu thuyết mới"""
		dialog = ctk.CTkInputDialog(text="Nhập tên bộ truyện/tiểu thuyết chữ mới:", title="Import Novel")
		input_name = dialog.get_input()
		if input_name and input_name.strip() != "":
			name = input_name.strip()
			self.mock_novels.append(name)
			self.refresh_novel_list()
			self.view_novel_workspace(name)
			messagebox.showinfo("Thành công", f"Đã khởi tạo phân hệ xử lý cho tác phẩm: {name}")
