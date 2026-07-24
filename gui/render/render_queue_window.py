import customtkinter as ctk
from tkinter import messagebox
import threading
import time

from ai.scene_splitter.shot import Shot
from core.episode_builder import EpisodeBuilder

class RenderQueueWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		self.shot_widgets = {}
		self.is_rendering = False

		# BỐ CỤC GIAO DIỆN LTX QUEUE MỚI CHUẨN CHATGPT
		self.title_lbl = ctk.CTkLabel(self, text="LTX Queue 2.0", font=ctk.CTkFont(size=18, weight="bold"))
		self.title_lbl.pack(padx=20, pady=15, anchor="w")
		
		self.subtitle_lbl = ctk.CTkLabel(self, text="Trình quản lý hàng đợi kết xuất tự động cấp độ Cú máy (Shot-level Render)", font=ctk.CTkFont(size=13, italic=True), text_color="gray")
		self.subtitle_lbl.pack(padx=20, pady=(0, 10), anchor="w")

		# Khung cuộn chứa danh sách các Shot xếp hàng (Giống hệt thiết kế hình ảnh)
		self.queue_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
		self.queue_container.pack(fill="both", expand=True, padx=15, pady=5)

		# NÚT BẤM TỐI THƯỢNG THEO ĐÚNG ĐẶC TẢ TRÊN ẢNH MẪU
		self.btn_generate = ctk.CTkButton(
			self, text="[ Generate Episode ]", fg_color="#C62828", hover_color="#B71C1C",
			font=ctk.CTkFont(size=14, weight="bold"), command=self.start_batch_episode_production
		)
		self.btn_generate.pack(padx=20, pady=15, fill="x")

	def start_batch_episode_production(self):
		"""Kích hoạt luồng xử lý tự động khi người dùng click nút Generate Episode"""
		if self.is_rendering:
			messagebox.showwarning("LTX Queue", "Hệ thống đang kết xuất một tập phim ngầm. Vui lòng chờ đợi!")
			return
			
		# Xóa sạch giao diện cũ để nạp danh sách Shot mới
		for widget in self.queue_container.winfo_children():
			widget.destroy()
		self.shot_widgets.clear()

		# Khởi tạo nhanh 4 Shots mẫu tăm tắp đúng tuyệt đối theo sơ đồ chữ của ChatGPT
		self.mock_shots = [
			Shot(id=10101, scene_id=101, index=1, context_type="establishing", camera="Wide", lens="24mm", movement="Static", duration=4.0, lighting="Day", seed="1", prompt="establishing shot", video_path="projects/cache/shot_10101.mp4"),
			Shot(id=10102, scene_id=101, index=2, context_type="action", camera="Medium", lens="50mm", movement="Static", duration=3.0, lighting="Day", seed="1", prompt="shot 02", video_path="projects/cache/shot_10102.mp4"),
			Shot(id=10103, scene_id=101, index=3, context_type="reaction", camera="Closeup", lens="85mm", movement="Static", duration=3.0, lighting="Day", seed="1", prompt="shot 03", video_path="projects/cache/shot_10103.mp4"),
			Shot(id=10104, scene_id=101, index=4, context_type="dialogue", camera="Closeup", lens="85mm", movement="Static", duration=3.5, lighting="Day", seed="1", prompt="shot 04", video_path="projects/cache/shot_10104.mp4")
		]

		# Vẽ bộ khung hàng đợi trạng thái ban đầu lên UI
		for shot in self.mock_shots:
			row_frame = ctk.CTkFrame(self.queue_container)
			row_frame.pack(fill="x", pady=4, padx=5)
			
			lbl_name = ctk.CTkLabel(row_frame, text=f"shot {shot.index:02d}", width=100, anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
			lbl_name.pack(side="left", padx=15, pady=10)
			
			progress_bar = ctk.CTkProgressBar(row_frame, width=250)
			progress_bar.set(0.0)
			progress_bar.pack(side="left", padx=20)
			
			lbl_status = ctk.CTkLabel(row_frame, text="Waiting", font=ctk.CTkFont(size=13), text_color="gray")
			lbl_status.pack(side="right", padx=20)
			
			self.shot_widgets[shot.id] = {"progress": progress_bar, "status": lbl_status}

		# Bật luồng đa luồng ngầm (Multi-threading) chạy tiến trình Render tuần tự
		threading.Thread(target=self._execute_render_queue_thread, daemon=True).start()

	def _execute_render_queue_thread(self):
		"""Luồng xử lý ngập kết xuất lần lượt từng Shot giống hệt Blender Render Queue"""
		self.is_rendering = True
		completed_paths = []

		for shot in self.mock_shots:
			widgets = self.shot_widgets[shot.id]
			widgets["status"].configure(text="Rendering...", text_color="#1F6AA5")
			
			# Giả lập thanh phần trăm Progress Bar tăng tốc chạy thời gian thực
			for progress in range(0, 101, 20):
				widgets["progress"].set(progress / 100)
				time.sleep(0.3) # Nhịp đẩy phần trăm
				
			widgets["status"].configure(text="Completed", text_color="#2E7D32")
			widgets["progress"].configure(progress_color="#2E7D32")
			completed_paths.append(shot.video_path)

		# --- KÍCH HOẠT ĐỘNG CƠ HẬU KỲ EPISODE BUILDER KHI TẤT CẢ SHOT HOÀN THÀNH ---
		builder = EpisodeBuilder(project_id="ToanDanTaoPhong", episode_number=1)
		final_video = builder.stitch_shots_into_episode(completed_paths)
		
		self.is_rendering = False
		messagebox.showinfo("AI Donghua Studio", f"Dây chuyền sản xuất v0.6 hoàn tất xuất phim dài tập!\n\nĐường dẫn tệp phim: {final_video}")