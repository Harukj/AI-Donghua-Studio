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
		"""
		[BƯỚC 3 - IMPORT DOCX]
		Kích hoạt hộp thoại chọn file Word và đổ toàn bộ nội dung thực tế lên màn hình giao diện
		"""
		from tkinter import filedialog, messagebox
		from core.services.novel_service import NovelService
		
		# 1. Mở hộp thoại hệ điều hành để người dùng chọn tệp .docx chuẩn theo ảnh mẫu
		file_path = filedialog.askopenfilename(
			filetypes=[("Word Documents", "*.docx")]
		)
		
		if file_path:
			try:
				# 2. Khởi tạo service xử lý
				novel_service = NovelService()
				
				# Tạm thời gán dự án làm việc hiện tại
				current_project = "ToanDanTaoPhong"
				
				# 3. Thực hiện đọc file thực tế, nhân bản tệp vào thư mục dự án và bóc tách phân chương
				result = novel_service.process_novel_import(current_project, file_path)
				
				# 4. Đổ tên tác phẩm được trích xuất từ tên file lên ô nhập liệu
				self.novel_form.entry_novel_title.delete(0, "end")
				self.novel_form.entry_novel_title.insert(0, result["novel_title"])
				
				# 5. Ghi đè danh sách chương giả lập bằng bộ dữ liệu thật bóc tách từ file Word
				self.novel_form.mock_chapters = result["chapters"]
				self.novel_form.render_chapters()
				
				# 6. Tự động tải nội dung chương đầu tiên lên bảng Textbox bên phải cho người dùng đọc
				self.novel_form.load_chapter_content(0)
				
				messagebox.showinfo(
					"Novel Import System", 
					f"Nạp thành công tệp truyện chữ điện ảnh!\nĐã lưu bản sao biệt lập vào thư mục của Project."
				)
				
			except Exception as e:
				messagebox.showerror("Lỗi hệ thống", f"Không thể đọc hoặc lưu file Word: {e}")
