import customtkinter as ctk
from tkinter import messagebox
from gui.novel.novel_form import NovelForm

class NovelWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Thiết lập lưới không gian chính
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=3)
		self.grid_rowconfigure(0, weight=1)
		
		self.selected_novel = None
		
		# 1. DANH SÁCH TÁC PHẨM BÊN TRÁI (NOVEL LIBRARY)
		self.left_frame = ctk.CTkFrame(self)
		self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		
		self.title_label = ctk.CTkLabel(
			self.left_frame, text="Novel Library", font=ctk.CTkFont(size=18, weight="bold")
		)
		self.title_label.pack(padx=15, pady=15, anchor="w")
		
		self.list_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
		self.list_frame.pack(padx=10, pady=5, fill="both", expand=True)
		
		# 2. KHU VỰC KHÔNG GIAN BIỂU MẪU XỬ LÝ CHI TIẾT BÊN PHẢI (WORKSPACE)
		self.right_frame = ctk.CTkFrame(self)
		self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
		
		# Nhúng trực tiếp NovelForm thương mại vào vùng không gian làm việc
		# Truyền hàm 'self.handle_docx_import' làm hành động callback khi bấm nút Import
		self.novel_form = NovelForm(self.right_frame, import_callback=self.handle_docx_import)
		self.novel_form.pack(fill="both", expand=True, padx=5, pady=5)
		
		# Dữ liệu tác phẩm chạy thử nghiệm ban đầu
		self.mock_novels = ["Toàn Dân Tạo Mộng - Quyển 1", "Đấu Phá Thương Khung"]
		self.refresh_novel_list()
		
		# Mặc định điền thử tên tác phẩm mẫu vào ô nhập liệu giống hệt ảnh của bạn
		self.novel_form.entry_novel_title.insert(0, "toàn dân tạo mộng")

	def refresh_novel_list(self):
		for widget in self.list_frame.winfo_children():
			widget.destroy()
		for novel_name in self.mock_novels:
			btn = ctk.CTkButton(
				self.list_frame, text=novel_name, anchor="w", height=38,
				fg_color="transparent", text_color=("#000000", "#FFFFFF"),
				command=lambda n=novel_name: self.select_novel_workspace(n)
			)
			btn.pack(fill="x", pady=2, padx=5)

	def select_novel_workspace(self, name):
		self.selected_novel = name
		self.novel_form.entry_novel_title.delete(0, "end")
		self.novel_form.entry_novel_title.insert(0, name.lower())
		print(f"Hệ thống: Đã kích hoạt không gian xử lý tệp văn bản cho: {name}")

	def handle_docx_import(self):
		"""Hàm xử lý khi click nút [ Import DOCX ] để nạp file từ hệ điều hành"""
		from tkinter import filedialog
		file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx"), ("Text Files", "*.txt")])
		if file_path:
			import os
			filename = os.path.basename(file_path)
			messagebox.showinfo("Novel Import System", f"Đã nạp tệp truyện '{filename}' thành công!\nHệ thống sẵn sàng bóc tách tự động phân chương.")
