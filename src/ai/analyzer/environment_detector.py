from sqlalchemy.orm import Session
from database.models.environment import EnvironmentModel
from core.logger import studio_logger

class RuleBasedEnvironmentDetector:
	def __init__(self, db_session: Session):
		"""Khởi tạo bộ quét bối cảnh Giai đoạn 1 (Rule-based) kết nối SQLite"""
		self.db = db_session

	def detect_environment_in_text(self, scene_text: str) -> dict:
		"""
		[GIAI ĐOẠN 1 - RULE-BASED ENVIRONMENT DETECTOR]
		Tự động quét so khớp tên địa điểm không gian trực tiếp từ 
		thư viện Environment Library với văn bản phân cảnh kịch bản.
		"""
		# 1. Truy vấn lấy danh sách bối cảnh không gian đang quản lý trong database
		db_envs = self.db.query(EnvironmentModel).all()
		
		if not db_envs:
			# Khởi tạo danh sách địa điểm mẫu dự phòng của ChatGPT để phục vụ tích kiểm
			known_locations = ["Học viện Long Dạng", "Ký túc xá", "Đấu trường", "Mạng Ước Mơ"]
		else:
			known_locations = [env.name for env in db_envs if env.name]

		detected_env = "Default Environment"
		scene_text_lower = scene_text.lower()

		# 2. THUẬT TOÁN SO KHỚP CHUỖI TĨNH (STRING MATCHING)
		for location in known_locations:
			if location.lower() in scene_text_lower:
				detected_env = location
				break # Tìm thấy không gian bối cảnh chính thì dừng lại để gán cảnh quay

		# Đóng gói xuất dữ liệu định dạng JSON/Dict sạch tương thích Prompt Engine
		output_json = {
			"environment": detected_env
		}
		
		studio_logger.logger.info(f"Rule-based Detector: Đã tự động so khớp bối cảnh không gian -> [{detected_env}]")
		return output_json
