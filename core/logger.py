import logging
import os
from datetime import datetime

class StudioLogger:
	def __init__(self, log_dir="logs"):
		"""Khởi tạo bộ ghi nhật ký tự động lưu file giống hệ thống của Unity hoặc Unreal Engine"""
		self.log_dir = log_dir
		if not os.path.exists(self.log_dir):
			os.makedirs(self.log_dir)

		# Định vị file lưu trữ nhật ký theo ngày
		log_filename = f"studio_{datetime.now().strftime('%Y-%m-%d')}.log"
		log_path = os.path.join(self.log_dir, log_filename)

		# Thiết lập cấu hình format chuẩn phần mềm thương mại
		self.logger = logging.getLogger("AI_Donghua_Studio")
		self.logger.setLevel(logging.INFO)

		# Tránh lặp lại handler khi khởi tạo nhiều lần
		if not self.logger.handlers:
			formatter = logging.Formatter("%(asctime)s [%(levelname)s] -> %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

			# Handler 1: Ghi dữ liệu trực tiếp ra màn hình Terminal để lập trình viên theo dõi
			console_handler = logging.StreamHandler()
			console_handler.setFormatter(formatter)
			self.logger.addHandler(console_handler)

			# Handler 2: Xuất dữ liệu lưu trữ thành file cứng (.log) để tra cứu sau này
			file_handler = logging.FileHandler(log_path, encoding="utf-8")
			file_handler.setFormatter(formatter)
			self.logger.addHandler(file_handler)

	# --- 5 HÀM GHI NHẬT KÝ ĐỘC QUYỀN THEO ĐẶC TẢ CỦA CHATGPT ---
	def log_import_novel(self, filename: str, status: str = "SUCCESS"):
		"""Ghi nhật ký hành động nạp tệp kịch bản truyện chữ"""
		self.logger.info(f"[IMPORT NOVEL] File: {filename} | Trạng thái: {status}")

	def log_generate_scene(self, scene_id: str, character_count: int, status: str = "SUCCESS"):
		"""Ghi nhật ký hành động bóc tách thực thể và tự trộn Prompt phân cảnh"""
		self.logger.info(f"[GENERATE SCENE] Phân cảnh: {scene_id} | Nhân vật tìm thấy: {character_count} | Trạng thái: {status}")

	def log_render_video(self, scene_id: str, progress: int, status: str = "RENDERING"):
		"""Ghi nhật ký hàng đợi kết xuất video theo thời gian thực"""
		self.logger.info(f"[RENDER VIDEO] Phân cảnh: {scene_id} | Tiến độ: {progress}% | Trạng thái: {status}")

	def log_export_episode(self, episode_num: int, duration_seconds: float, export_path: str):
		"""Ghi nhật ký hành động đóng gói xuất phim dài tập YouTube (Final Render)"""
		self.logger.info(f"[EXPORT EPISODE] Tập phim: {episode_num:02d} | Thời lượng: {duration_seconds}s | Tệp xuất: {export_path}")

	def log_open_project(self, project_name: str):
		"""Ghi nhật ký hành động mở không gian làm việc của dự án"""
		self.logger.info(f"[OPEN PROJECT] Kích hoạt không gian làm việc dự án: '{project_name}'")

# Khởi tạo một đối tượng Logger duy nhất dùng chung cho toàn bộ ứng dụng (Singleton)
studio_logger = StudioLogger()
