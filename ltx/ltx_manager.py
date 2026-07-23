import time
import threading
from analyzer.scene_object import Scene

class LTXManager:
	def __init__(self):
		"""Khởi tạo quản lý hàng đợi kết xuất video (Render Queue)"""
		self.render_queue = []          # Danh sách các Scene đang xếp hàng chờ
		self.current_rendering = None   # Phân cảnh hiện tại đang được xử lý
		self.completed_scenes = {}      # Lưu trữ các Scene đã render xong và đường dẫn video thành phẩm
		self.is_processing = False      # Trạng thái cờ hiệu kiểm soát luồng hoạt động
		self.status_callback = None     # Hàm callback dùng để cập nhật tiến trình hiển thị lên giao diện GUI

	def set_status_callback(self, callback_func):
		"""Đăng ký hàm callback để đẩy trạng thái hiển thị thời gian thực lên giao diện người dùng"""
		self.status_callback = callback_func

	def add_to_queue(self, scene_object: Scene):
		"""[LTX Queue] Đẩy một phân cảnh Object sạch vào hàng đợi kết xuất"""
		self.render_queue.append(scene_object)
		print(f"LTX Queue: Đã thêm Phân cảnh [{scene_object.id}] vào hàng đợi chờ xử lý.")
		
		# Tự động kích hoạt bộ xử lý hàng đợi nếu hệ thống đang rảnh
		if not self.is_processing:
			threading.Thread(target=self._process_queue, daemon=True).start()

	def _process_queue(self):
		"""Hàm lõi chạy ngầm (Background Thread) để xử lý tuần tự từng phân cảnh trong hàng đợi"""
		self.is_processing = True
		
		while self.render_queue:
			# Lấy phân cảnh đầu tiên ra khỏi hàng đợi xử lý
			self.current_rendering = self.render_queue.pop(0)
			scene_id = self.current_rendering.id
			
			print(f"LTX Manager: Bắt đầu kết xuất Phân cảnh [{scene_id}]...")
			
			# --- GIẢ LẬP TIẾN TRÌNH RENDERING (Thanh Progress bar trong thiết kế của ChatGPT) ---
			for progress in range(0, 101, 10):
				# Phát tín hiệu báo cáo tiến độ về cho giao diện (GUI) cập nhật thanh Progress bar
				if self.status_callback:
					self.status_callback(scene_id, "Rendering", progress)
				time.sleep(0.5) # Giả lập thời gian AI xử lý tính toán khung hình (0.5 giây cho 10%)
			
			# Giả lập đường dẫn file video thành phẩm xuất ra sau khi render hoàn tất
			mock_video_path = f"output/videos/{scene_id.lower()}_render.mp4"
			self.completed_scenes[scene_id] = mock_video_path
			
			print(f"LTX Manager: Hoàn thành kết xuất Phân cảnh [{scene_id}] -> {mock_video_path}")
			
			# Phát tín hiệu báo cáo phân cảnh đã hoàn thành [Done]
			if self.status_callback:
				self.status_callback(scene_id, "Done", 100)
				
		self.current_rendering = None
		self.is_processing = False
		print("LTX Manager: Hàng đợi kết xuất trống. Toàn bộ kịch bản phân cảnh đã hoàn thành sinh phim.")
