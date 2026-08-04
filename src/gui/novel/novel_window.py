import customtkinter as ctk
from tkinter import messagebox
from src.gui.novel.novel_form import NovelForm

class NovelWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		from src.database.session import SessionLocal
		self.db = SessionLocal() # Khởi tạo session kết nối SQLite
		
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
		"""Kích hoạt động cơ lõi 9 bước NovelPipeline khi Import file truyện chữ"""
		from tkinter import filedialog, messagebox
		from src.pipeline.novel_pipeline import NovelPipeline  # Import bộ điều phối luồng mới
		from src.core.logger import studio_logger
		import os
				
			# Kích hoạt bộ ghi nhật ký chuẩn Unreal Engine
		studio_logger.log_import_novel(filename=os.path.basename(file_path), status="SUCCESS")
		# 1. Cho người dùng lựa chọn tệp .docx từ hệ điều hành máy tính
		file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
		if file_path:
			try:
				# 2. Khởi tạo Pipeline nạp phiên làm việc dữ liệu SQLite
				pipeline = NovelPipeline(self.db)
				current_project = "ToanDanTaoPhong"
				
				# 3. Chạy kích hoạt toàn bộ luồng 9 bước tự động
				result = pipeline.run_pipeline(current_project, file_path)
				
				self.novel_form.entry_novel_title.delete(0, "end")
				self.novel_form.entry_novel_title.insert(0, result["novel_title"])
				
				chapters_ui_data = []
				for scene in result["scenes"]:
					chapters_ui_data.append({
						"title": f"#{scene.id.lower()}",
						"text": f"Nhân vật: {', '.join(scene.characters)}\nBối cảnh: {', '.join(scene.environments)}\nThời lượng: {scene.duration}s\n\nKịch bản văn học:\n{scene.summary}"
					})
				
				self.novel_form.mock_chapters = chapters_ui_data
				self.novel_form.render_chapters()
				self.novel_form.load_chapter_content(0)
				
				messagebox.showinfo("AI Donghua Studio", "Hệ thống Đạo diễn AI đã hoàn thành bóc tách 9 bước tuần tự thành công!")
			except Exception as e:
				messagebox.showerror("Lỗi hệ thống", f"Luồng xử lý Pipeline v1.0 gặp sự cố: {e}")