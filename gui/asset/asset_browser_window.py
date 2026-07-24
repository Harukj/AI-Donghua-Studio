import customtkinter as ctk
from database.session import SessionLocal
from database.repositories.asset_repository import AssetRepository

class AssetBrowserWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Khởi tạo kết nối database để quét danh sách file vật lý lưu trong bảng assets
		self.db = SessionLocal()
		self.asset_repo = AssetRepository(self.db)
		
		# Thiết lập bố cục lưới (Cột 0: Cây thư mục lề trái, Cột 1: Vùng hiển thị file lề phải)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=3)
		self.grid_rowconfigure(0, weight=1)
		
		# 1. PHÂN KHU BÊN TRÁI: CÂY THƯ MỤC TÀI NGUYÊN (ASSETS FOLDERS)
		self.folder_panel = ctk.CTkFrame(self)
		self.folder_panel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
		
		self.lbl_assets_title = ctk.CTkLabel(self.folder_panel, text="Assets", font=ctk.CTkFont(size=16, weight="bold"))
		self.lbl_assets_title.pack(padx=15, pady=15, anchor="w")
		
		# Danh sách các phân khu thư mục con chuẩn hóa từ ảnh mẫu của ChatGPT
		self.studio_folders = ["characters", "environment", "props", "audio", "fx"]
		self.folder_scroll = ctk.CTkScrollableFrame(self.folder_panel, fg_color="transparent")
		self.folder_scroll.pack(fill="both", expand=True, padx=5, pady=5)
		
		# 2. PHÂN KHU BÊN PHẢI: KHÔNG GIAN DUYỆT TỆP TIN CHI TIẾT (FILE GRID DISPLAY)
		self.file_panel = ctk.CTkFrame(self)
		self.file_panel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
		
		self.lbl_workspace_title = ctk.CTkLabel(self.file_panel, text="Content Browser", font=ctk.CTkFont(size=16, weight="bold"))
		self.lbl_workspace_title.pack(padx=20, pady=15, anchor="w")
		
		self.file_scroll = ctk.CTkScrollableFrame(self.file_panel, fg_color="transparent")
		self.file_scroll.pack(fill="both", expand=True, padx=15, pady=5)
		
		# Vẽ bộ nút bấm thư mục và mặc định tải phân khu đầu tiên
		self.render_folder_tree()
		self.load_folder_contents("characters")

	def render_folder_tree(self):
		"""Vẽ danh sách cây thư mục viết thường lề trái"""
		for folder in self.studio_folders:
			btn = ctk.CTkButton(
				self.folder_scroll, text=f"📁  {folder}", anchor="w", height=35,
				fg_color="transparent", text_color=("#000000", "#FFFFFF"),
				font=ctk.CTkFont(size=13),
				command=lambda f=folder: self.load_folder_contents(f)
			)
			btn.pack(fill="x", pady=2, padx=5)

	def load_folder_contents(self, folder_name):
		"""[ASSET BROWSER CORE DISPLAY] Quét database lọc file và vẽ danh sách tệp tin lên lề phải giống Unity"""
		# Highlight trạng thái thư mục đang chọn bên lề trái
		for idx, btn in enumerate(self.folder_scroll.winfo_children()):
			if self.studio_folders[idx] == folder_name:
				btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
			else:
				btn.configure(fg_color="transparent")

		# Xóa sạch các icon file cũ ở khung nhìn lề phải
		for widget in self.file_scroll.winfo_children():
			widget.destroy()
			
		self.lbl_workspace_title.configure(text=f"Assets > {folder_name}")
		
		# Truy vấn cơ sở dữ liệu thật thông qua AssetRepository để lấy danh sách file thuộc phân khu này
		current_project = "ToanDanTaoPhong"
		db_files = self.asset_repo.get_assets_by_type(current_project, folder_name)
		
		if not db_files:
			# Nếu dự án mới chưa nạp file thật, hiển thị bản ghi dữ liệu mẫu của ChatGPT (Ví dụ: Tô Mộc) để test giao diện
			if folder_name == "characters":
				mock_file_lbl = ctk.CTkButton(self.file_scroll, text="👤  Tô Mộc (Profile Model)", height=40, anchor="w", fg_color="transparent", text_color=("#000000", "#FFFFFF"))
				mock_file_lbl.pack(fill="x", pady=2)
			else:
				empty_lbl = ctk.CTkLabel(self.file_scroll, text="Thư mục trống. Chưa có tài nguyên tệp tin.", text_color="gray", font=ctk.CTkFont(size=13, italic=True))
				empty_lbl.pack(pady=20)
			return

		# Duyệt mảng và vẽ danh sách file thật có trong SQLite ra màn hình
		for file in db_files:
			icon = "🎵 " if folder_name == "audio" else "📄 "
			file_btn = ctk.CTkButton(
				self.file_scroll, text=f"{icon} {file.name}", anchor="w", height=40,
				fg_color="transparent", text_color=("#000000", "#FFFFFF"),
				font=ctk.CTkFont(size=13)
			)
			file_btn.pack(fill="x", pady=2)

	def __del__(self):
		try: self.db.close()
		except: pass
