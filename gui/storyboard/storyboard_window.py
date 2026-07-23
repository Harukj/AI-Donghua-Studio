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
		self.detail_title.pack(padx=20, pady=15, anchor="w")
		
		# Nhúng trực tiếp biểu mẫu cấu hình StoryboardForm vào vùng nhìn bên phải
		from gui.storyboard.storyboard_form import StoryboardForm
		self.storyboard_form = StoryboardForm(self.right_frame_layout_container(), approve_callback=self.approve_current_scene)
		# Tạm thời ẩn form đi, chỉ hiển thị khi người dùng chọn scene thực tế
		
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
		self.selected_scene_id = scene_db_id
		scene = self.storyboard_repo.get_by_id(scene_db_id)
		
		if scene:
			# Ẩn nhãn thông báo mặc định
			self.status_lbl.pack_forget()
			self.detail_title.configure(text=f"Cấu hình: Scene {scene.index:03d}")
			
			# Đóng gói dữ liệu bóc tách từ SQLite khớp 100% với form của ChatGPT
			ui_data = {
				"character": scene.characters or "Tô Mộc",
				"environment": scene.environments or "Ký túc xá",
				"camera": scene.camera or "Wide Shot",
				"mood": scene.mood or "Mysterious",
				"duration": scene.duration or 5.0,
				"prompt": scene.prompt or f"Masterpiece, Chinese Donghua style, wide shot, Tô Mộc in dormitory, mysterious atmosphere, cinematic lighting, 16:9",
				"status": scene.status
			}
			
			# Gọi form tự động cập nhật hiển thị lên màn hình phải
			self.storyboard_form.update_form_display(ui_data)
			self.storyboard_form.pack(fill="both", expand=True, padx=10, pady=5)

	def approve_current_scene(self):
		"""Hành động khi người dùng nhấn nút Duyệt phim: Đẩy trạng thái sang Approved"""
		if self.selected_scene_id:
			self.storyboard_repo.update_scene_status(self.selected_scene_id, "Approved")
			messagebox.showinfo("AI Donghua Studio", "Đã phê duyệt phân cảnh kịch bản điện ảnh!\nPhân cảnh đã được chuyển trạng thái chờ gửi sang LTX Render Queue.")
			self.load_scene_details(self.selected_scene_id)


	def __del__(self):
		try: self.db.close()
		except: pass
