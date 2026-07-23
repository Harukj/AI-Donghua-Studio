import customtkinter as ctk

class NovelForm(ctk.CTkFrame):
	def __init__(self, parent, import_callback):
		super().__init__(parent, fg_color="transparent")
		self.import_callback = import_callback
		self.selected_chapter_index = None
		
		# Khởi tạo bố cục lưới bên trong Form (Cột 0: Quản lý chương, Cột 1: Hiển thị nội dung chữ)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=2)
		self.grid_rowconfigure(0, weight=1)
		
		# 1. KHU VỰC BÊN TRÁI FORM: DANH SÁCH CHƯƠNG TRUYỆN
		self.chapter_panel = ctk.CTkFrame(self)
		self.chapter_panel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
		
		# Nút bấm nạp tệp văn bản thương mại [ Import DOCX ] theo đúng ảnh mẫu
		self.btn_import_docx = ctk.CTkButton(
			self.chapter_panel,
			text="[ Import DOCX ]",
			fg_color="#1F6AA5",
			hover_color="#144871",
			font=ctk.CTkFont(size=13, weight="bold"),
			command=self.import_callback
		)
		self.btn_import_docx.pack(padx=15, pady=15, fill="x")
		
		# Ô nhập và hiển thị Tên tác phẩm (Ví dụ: toàn dân tạo mộng)
		self.title_lbl = ctk.CTkLabel(self.chapter_panel, text="Tác phẩm:", anchor="w", font=ctk.CTkFont(size=12, weight="bold"))
		self.title_lbl.pack(padx=15, pady=(5, 0), fill="x")
		
		self.entry_novel_title = ctk.CTkEntry(self.chapter_panel, placeholder_text="Tên truyện chữ...")
		self.entry_novel_title.pack(padx=15, pady=5, fill="x")
		
		# Tiêu đề danh mục Chương
		self.chapter_lbl = ctk.CTkLabel(self.chapter_panel, text="Chương", anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
		self.chapter_lbl.pack(padx=15, pady=(15, 5), fill="x")
		
		# Khung cuộn chứa các chương truyện tự động bóc tách
		self.chapter_scroll = ctk.CTkScrollableFrame(self.chapter_panel, fg_color="transparent")
		self.chapter_scroll.pack(padx=10, pady=5, fill="both", expand=True)
		
		# 2. KHU VỰC BÊN PHẢI FORM: VÙNG ĐỌC VÀ CHỈNH SỬA VĂN BẢN (NỘI DUNG CHƯƠNG)
		self.content_panel = ctk.CTkFrame(self)
		self.content_panel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
		
		self.content_lbl = ctk.CTkLabel(self.content_panel, text="Nội dung chương", anchor="w", font=ctk.CTkFont(size=14, weight="bold"))
		self.content_lbl.pack(padx=20, pady=15, fill="x")
		
		# Vùng văn bản Textbox lớn để hiển thị toàn bộ nội dung truyện thô
		self.txt_chapter_content = ctk.CTkTextbox(self.content_panel, font=ctk.CTkFont(size=13))
		self.txt_chapter_content.pack(padx=15, pady=(0, 15), fill="both", expand=True)
		
		# Dữ liệu chương giả lập khớp 100% với danh sách hiển thị trên ảnh của bạn
		self.mock_chapters = [
			{"title": "#1 khởi đầu", "text": "Đây là nội dung văn học thô của Chương 1: Khởi đầu...\nĐạo diễn AI sẽ dựa vào đây để bóc tách thực thể phân cảnh điện ảnh."},
			{"title": "#2 thiên tài", "text": "Nội dung Chương 2: Thiên tài xuất thế...\nTô Mộc bắt đầu bộc lộ tư chất đặc dị trong không gian Dream Network."},
			{"title": "#3 tiến vào mộng võng", "text": "Nội dung Chương 3: Tiến vào mộng võng...\nBầu không khí trở nên vô cùng hoành tráng và tráng lệ (Epic mood)."}
		]
		self.render_chapters()

	def render_chapters(self):
		"""Hàm quét danh sách mảng và vẽ các nút bấm chương lên giao diện lề trái của form"""
		for widget in self.chapter_scroll.winfo_children():
			widget.destroy()
			
		for index, ch in enumerate(self.mock_chapters):
			btn = ctk.CTkButton(
				self.chapter_scroll,
				text=ch["title"],
				anchor="w",
				height=35,
				fg_color="transparent",
				text_color=("#000000", "#FFFFFF"),
				command=lambda i=index: self.load_chapter_content(i)
			)
			btn.pack(fill="x", pady=2, padx=5)

	def load_chapter_content(self, index):
		"""Hành động khi người dùng click vào một chương: Đổ văn bản vào Textbox bên phải"""
		self.selected_chapter_index = index
		chapter_data = self.mock_chapters[index]
		
		# Highlight trạng thái nút bấm chương đang được chọn
		for idx, btn in enumerate(self.chapter_scroll.winfo_children()):
			if idx == index:
				btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
			else:
				btn.configure(fg_color="transparent")
				
		# Cập nhật văn bản chi tiết vào vùng hiển thị nội dung chương
		self.txt_chapter_content.delete("1.0", "end")
		self.txt_chapter_content.insert("1.0", chapter_data["text"])
