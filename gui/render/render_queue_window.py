import customtkinter as ctk
from ltx.ltx_manager import LTXManager
from analyzer.scene_object import Scene

class RenderQueueWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Khởi tạo bộ máy quản lý kết xuất đa luồng
		self.ltx_manager = LTXManager()
		self.ltx_manager.set_status_callback(self.update_gui_progress_callback)
		
		# Khay lưu trữ danh sách các widget thanh tiến trình của từng Scene trên UI
		self.scene_widgets = {}

		# Thiết lập bố cục tiêu đề
		self.title_lbl = ctk.CTkLabel(self, text="Render Queue (Blender Style)", font=ctk.CTkFont(size=18, weight="bold"))
		self.title_lbl.pack(padx=20, pady=15, anchor="w")
		
		self.subtitle_lbl = ctk.CTkLabel(self, text="Hàng đợi kết xuất clip hoạt hình 3D Donghua tự động theo thời gian thực", font=ctk.CTkFont(size=13, italic=True), text_color="gray")
		self.subtitle_lbl.pack(padx=20, pady=(0, 10), anchor="w")

		# Khung cuộn chứa danh sách các phân cảnh đang render giống ảnh mẫu ChatGPT
		self.queue_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
		self.queue_container.pack(fill="both", expand=True, padx=15, pady=5)

		# Nút bấm giả lập hành động bấm kích hoạt Render toàn bộ tập phim
		self.btn_start_render = ctk.CTkButton(
			self, text="[ Start Batch Rendering Episode 01 ]", fg_color="#1F6AA5", hover_color="#144871",
			font=ctk.CTkFont(size=14, weight="bold"), command=self.trigger_batch_render
		)
		self.btn_start_render.pack(padx=20, pady=15, fill="x")

	def trigger_batch_render(self):
		"""Hành động khi bấm nút: Đẩy danh sách phân cảnh mẫu của ChatGPT vào hàng đợi"""
		# Xóa sạch giao diện cũ trước khi render
		for widget in self.queue_container.winfo_children():
			widget.destroy()
		self.scene_widgets.clear()

		# Khởi tạo 3 phân cảnh mẫu đúng tuyệt đối theo sơ đồ khối của ChatGPT
		mock_scenes = [
			Scene(id="scene 001", chapter=1, title="Mở mắt", summary="Tô Mộc mở mắt.", characters=["Tô Mộc"], environments=["Ký túc xá"], props=[], dialogues=[], duration=5.0),
			Scene(id="scene 002", chapter=1, title="Giáo viên", summary="Giáo viên bước vào.", characters=["Giáo viên"], environments=["Học viện"], props=[], dialogues=[], duration=5.0),
			Scene(id="scene 003", chapter=1, title="Kinh ngạc", summary="Mọi người kinh ngạc.", characters=["Học sinh"], environments=["Học viện"], props=[], dialogues=[], duration=5.0)
		]

		# Duyệt mảng để vẽ bộ khung giao diện trạng thái 'Waiting' ban đầu lên màn hình
		for scene in mock_scenes:
			row_frame = ctk.CTkFrame(self.queue_container)
			row_frame.pack(fill="x", pady=4, padx=5)
			
			lbl_name = ctk.CTkLabel(row_frame, text=scene.id, width=100, anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
			lbl_name.pack(side="left", padx=15, pady=10)
			
			# Thanh tiến trình Progress bar ảo của CustomTkinter
			progress_bar = ctk.CTkProgressBar(row_frame, width=250)
			progress_bar.set(0.0)
			progress_bar.pack(side="left", padx=20)
			
			lbl_status = ctk.CTkLabel(row_frame, text="waiting", font=ctk.CTkFont(size=13, weight="medium"), text_color="gray")
			lbl_status.pack(side="right", padx=20)
			
			# Lưu các widget điều khiển vào khay bộ nhớ để cập nhật luồng ngầm về sau
			self.scene_widgets[scene.id] = {
				"progress": progress_bar,
				"status": lbl_status,
				"frame": row_frame
			}

		# Đẩy loạt đối tượng kịch bản sạch vào lõi đa luồng LTXManager để tự động kết xuất tuần tự
		for scene in mock_scenes:
			self.ltx_manager.add_to_queue(scene)

	def update_gui_progress_callback(self, scene_id, status, progress_value):
		"""HÀM CALLBACK NHẬN TÍN HIỆU ĐA LUỒNG: Tự động cập nhật giao diện Progress Bar từ luồng chạy ngầm"""
		if scene_id in self.scene_widgets:
			widgets = self.scene_widgets[scene_id]
			
			if status == "Rendering":
				# Chuyển đổi giá trị từ thang 100 sang thang số thực 0.0 - 1.0 của CustomTkinter
				widgets["progress"].set(progress_value / 100)
				widgets["status"].configure(text="rendering...", text_color="#1F6AA5")
			elif status == "Done":
				widgets["progress"].set(1.0)
				widgets["progress"].configure(progress_color="#2E7D32") # Đổi sang màu xanh lá khi xong
				widgets["status"].configure(text="completed", text_color="#2E7D32")
