import customtkinter as ctk
from tkinter import messagebox
from database.session import SessionLocal
from database.repositories.asset_repository import AssetRepository

class AssetBrowserWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Khởi tạo kết nối database và kho lưu trữ repository chuyên trách v1.0
		self.db = SessionLocal()
		self.asset_repo = AssetRepository(self.db)
		self.selected_folder = "characters"
		
		# Thiết lập bố cục lưới (Cột 0: Thư mục lề trái, Cột 1: Vùng duyệt file lề phải)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=3)
		self.grid_rowconfigure(0, weight=1)
		
		# 1. PHÂN VÙNG BÊN TRÁI: CÂY THƯ MỤC TÀI NGUYÊN (ASSETS FOLDERS)
		self.folder_panel = ctk.CTkFrame(self)
		self.folder_panel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
		
		self.lbl_assets_title = ctk.CTkLabel(self.folder_panel, text="Assets", font=ctk.CTkFont(size=16, weight="bold"))
		self.lbl_assets_title.pack(padx=15, pady=15, anchor="w")
		
		self.studio_folders = ["characters", "environment", "props", "effects", "audio", "reference_images"]
		self.folder_scroll = ctk.CTkScrollableFrame(self.folder_panel, fg_color="transparent")
		self.folder_scroll.pack(fill="both", expand=True, padx=5, pady=5)
		
		# 2. PHÂN VÙNG BÊN PHẢI: KHÔNG GIAN DUYỆT TỆP TIN CHI TIẾT (FILE GRID DISPLAY)
		self.file_panel = ctk.CTkFrame(self)
		self.file_panel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
		
		self.lbl_workspace_title = ctk.CTkLabel(self.file_panel, text="Content Browser", font=ctk.CTkFont(size=16, weight="bold"))
		self.lbl_workspace_title.pack(padx=20, pady=15, anchor="w")
		
		self.file_scroll = ctk.CTkScrollableFrame(self.file_panel, fg_color="transparent")
		self.file_scroll.pack(fill="both", expand=True, padx=15, pady=5)
		
		# Định nghĩa tập dữ liệu mẫu chuẩn hóa 100% khớp theo sơ đồ cây của ChatGPT
		self.mock_asset_data = {
			"characters": [("👤", "Tô Mộc"), ("doc_info", "Lâm Uyển")],
			"environment": [("🏙️", "Long Dạng"), ("🏫", "Học Viện")],
			"props": [("⚔️", "Kiếm"), ("💎", "Bảo Vật")],
			"effects": [("🔥", "Lửa"), ("💨", "Khói")],
			"audio": [("🎵", "Nhạc nền thô")],
			"reference_images": [("🖼️", "Concept Art Tô Mộc")]
		}
		
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
		"""Quét database lọc file và vẽ danh sách tệp tin lên lề phải giống Unity"""
		self.selected_folder = folder_name
		
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
		
		# 1. TRUY VẤN DỮ LIỆU THẬT TỪ DATABASE SQLITE TRƯỚC
		current_project = "ToanDanTaoPhong"
		db_files = self.asset_repo.get_assets_by_type(current_project, folder_name)
		
		# 2. NẾU DATABASE CHƯA CÓ FILE THẬT, TỰ ĐỘNG NẠP MOCK DATA THEO ẢNH CHATGPT
		if not db_files:
			mock_list = self.mock_asset_data.get(folder_name, [])
			if not mock_list:
				empty_lbl = ctk.CTkLabel(self.file_scroll, text="Thư mục trống.", text_color="gray", font=ctk.CTkFont(size=13, italic=True))
				empty_lbl.pack(pady=20)
				return
				
			for icon, name in mock_list:
				file_btn = ctk.CTkButton(
					self.file_scroll, text=f"{icon}  {name}", anchor="w", height=40,
					fg_color="transparent", text_color=("#000000", "#FFFFFF"),
					font=ctk.CTkFont(size=13),
					command=lambda n=name: self.on_asset_file_clicked(n)
				)
				file_btn.pack(fill="x", pady=2)
			return

		# 3. NẾU CÓ DỮ LIỆU THẬT, VẼ FILE THỰC TẾ
		for file in db_files:
			icon = "🎵 " if folder_name == "audio" else "📄 "
			file_btn = ctk.CTkButton(
				self.file_scroll, text=f"{icon}  {file.name}", anchor="w", height=40,
				fg_color="transparent", text_color=("#000000", "#FFFFFF"),
				font=ctk.CTkFont(size=13),
				command=lambda n=file.name: self.on_asset_file_clicked(n)
			)
			file_btn.pack(fill="x", pady=2)

	def on_asset_file_clicked(self, asset_name):
		"""
		[LUỒNG UX: KHI CLICK]
		Bắt sự kiện nhấp chuột chọn tệp tin tài nguyên theo đặc tả thiết kế của ChatGPT.
		Sẵn sàng mở rộng để nạp thuộc tính lên bảng Inspector lề phải ở bước sau.
		"""
		print(f"Hệ thống Engine: Người dùng đã click chọn tài nguyên -> [{asset_name}]")
		# Tạm thời thông báo trạng thái kết nối tương tác
		messagebox.showinfo("Asset Browser", f"Đã kích hoạt vùng nhìn thực thể cho: {asset_name}\n\nLuồng xử lý mở bảng Inspector chi tiết đang chờ đặc tả từ phần 'Khi click' của ChatGPT.")

	def __del__(self):
		try: self.db.close()
		except: pass
