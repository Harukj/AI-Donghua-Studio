import customtkinter as ctk
from tkinter import messagebox
from database.session import SessionLocal
from database.repositories.storyboard_repository import StoryboardRepository

class StoryboardWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Khởi tạo phiên kết nối database và kho lưu trữ repository chuyên trách v1.0
		self.db = SessionLocal()
		self.storyboard_repo = StoryboardRepository(self.db)
		self.selected_scene_id = None
		
		# Thiết lập bố cục lưới (Cột 0: Khung danh kịch bản phân cảnh, Cột 1: Khung cấu hình chi tiết)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		
		# 1. PHÂN VÙNG BÊN TRÁI: DANH SÁCH BẢNG PHÂN CẢNH (KHI CHỌN STORYBOARD)
		self.left_panel = ctk.CTkFrame(self)
		self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		
		self.title_lbl = ctk.CTkLabel(
			self.left_panel, text="Storyboard Workspace", font=ctk.CTkFont(size=18, weight="bold")
		)
		self.title_lbl.pack(padx=15, pady=15, anchor="w")
		
		# Tên tập phim hiện hành hiển thị đúng theo ảnh mẫu của ChatGPT
		self.episode_lbl = ctk.CTkLabel(
			self.left_panel, text="Episode 01", font=ctk.CTkFont(size=14, weight="medium", italic=True), text_color="gray"
		)
		self.episode_lbl.pack(padx=15, pady=(0, 10), anchor="w")
		
		self.separator = ctk.CTkLabel(self.left_panel, text="---------------------------------------------------", text_color="gray")
		self.separator.pack(padx=15, pady=5)
		
		# Khung cuộn chứa danh sách các phân cảnh (Scenes List)
		self.scenes_scroll = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
		self.scenes_scroll.pack(padx=10, pady=5, fill="both", expand=True)
		
		# 2. PHÂN VÙNG BÊN PHẢI: BẢNG TRÌNH ĐIỀU KHIỂN CHI TIẾT CẢNH QUAY (KHI CHỌN SCENE)
		self.right_panel = ctk.CTkFrame(self)
		self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
		
		self.detail_title = ctk.CTkLabel(
			self.right_panel, text="Thông số góc quay & AI Prompt", font=ctk.CTkFont(size=16, weight="bold")
		)
		self.detail_title.pack(padx=20, pady=20, anchor="w")
		
		self.status_lbl = ctk.CTkLabel(
			self.right_panel, text="Vui lòng click chọn một phân cảnh kịch bản ở lề trái\nđể cấu hình thông số điện ảnh AI chi tiết.",
			font=ctk.CTkFont(size=13, italic=True)
		)
		self.status_lbl.pack(expand=True)
		
		# Tự động nạp dữ liệu mẫu ban đầu để kiểm tra giao diện đúng thiết kế
		self.initialize_mock_storyboard_data()
		
		# Vẽ danh sách phân cảnh lên màn hình lề trái
		self.refresh_scenes_list()

	def initialize_mock_storyboard_data(self):
		"""Tự động chèn kịch bản phân cảnh mẫu của ChatGPT vào file SQLite nếu bảng trống"""
		from database.models.storyboard import StoryboardSceneModel
		if self.db.query(StoryboardSceneModel).count() == 0:
			mock_scenes = [
				{"index": 1, "summary": "Tô Mộc mở mắt."},
				{"index": 2, "summary": "Giáo viên bước vào."},
				{"index": 3, "summary": "Cả lớp kinh ngạc."}
			]
			for idx, scene in enumerate(mock_scenes, start=1):
				self.storyboard_repo.create({
					"chapter_id": 1,
					"index": scene["index"],
					"summary": scene["summary"],
					"project_id": "ToanDanTaoPhong",
					"status": "draft"
				})

	def refresh_scenes_list(self):
		"""Tải dữ liệu thật từ bảng 'scenes' lên UI theo đúng cấu trúc chuỗi kịch bản của ChatGPT"""
		for widget in self.scenes_scroll.winfo_children():
			widget.destroy()
			
		# Lấy toàn bộ phân cảnh thuộc chương 1 ra sắp xếp theo thứ tự index
		db_scenes = self.storyboard_repo.get_scenes_by_chapter(chapter_id=1)
		
		for scene in db_scenes:
			# Nối chuỗi kịch bản hiển thị đúng định dạng: #001 Nội dung hành động thô
			display_text = f"# {scene.index:03d}  {scene.summary}"
			
			btn = ctk.CTkButton(
				self.scenes_scroll, text=display_text, anchor="w", height=38,
				fg_color="transparent", text_color=("#000000", "#FFFFFF"),
				font=ctk.CTkFont(size=13),
				command=lambda s_id=scene.id: self.load_scene_details(s_id)
			)
			btn.pack(fill="x", pady=3, padx=5)

	def load_scene_details(self, scene_db_id):
		"""Hành động khi click chọn vào một Scene cụ thể: Chuẩn bị nạp form thuộc tính ở bước sau"""
		self.selected_scene_id = scene_db_id
		
		# Highlight nút đang chọn trong danh sách cuộn
		for idx, btn in enumerate(self.scenes_scroll.winfo_children()):
			if db_scene := self.db.query(self.storyboard_repo.model).filter_by(chapter_id=1).order_by(self.storyboard_repo.model.index.asc()).all():
				if db_scene[idx].id == scene_db_id:
					btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
				else:
					btn.configure(fg_color="transparent")

		scene = self.storyboard_repo.get_by_id(scene_db_id)
		if scene:
			for widget in self.right_panel.winfo_children():
				if widget != self.detail_title: widget.pack_forget()
				
			self.detail_title.configure(text=f"Cấu hình: Scene {scene.index:03d}")
			self.status_lbl.configure(text=f"Hành động thô: '{scene.summary}'\n\n[Trạng thái sản xuất: {scene.status.upper()}]\n\nCơ chế nạp Form thuộc tính chi tiết đang chờ đặc tả từ nút cuộn ở Bước 3...")
			self.status_lbl.pack(expand=True)

	def __del__(self):
		try: self.db.close()
		except: pass
