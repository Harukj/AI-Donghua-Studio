from sqlalchemy.orm import Session
from src.database.models.character import CharacterModel
from src.core.logger import studio_logger

class RuleBasedCharacterDetector:
	def __init__(self, db_session: Session):
		"""Khởi tạo bộ quét nhân vật Giai đoạn 1 (Rule-based) kết nối SQLite"""
		self.db = db_session

	def detect_characters_in_text(self, scene_text: str) -> dict:
		"""
		[GIAI ĐOẠN 1 - RULE-BASED DETECTOR]
		Không dùng AI tốn kém. Tự động quét so khớp tên nhân vật trực tiếp 
		từ cơ sở dữ liệu Character Bible với văn bản phân cảnh kịch bản.
		Trả về định dạng cấu trúc JSON sạch khớp 100% đặc tả của ChatGPT.
		"""
		# 1. Truy vấn lấy toàn bộ danh sách tên nhân vật đang có trong thư viện Character Bible
		db_characters = self.db.query(CharacterModel).all()
		
		# Khởi tạo danh sách nhân vật mẫu dự phòng của dự án nếu bảng database đang trống (Mục đích tích kiểm)
		if not db_characters:
			known_names = ["Tô Mộc", "Lâm Uyển", "Triệu Phong"]
		else:
			# Trích xuất lấy cột Tên và Biệt danh của các nhân vật trong DB
			known_names = [char.name for char in db_characters if char.name]
			# Bổ sung thêm biệt danh nếu có để tránh bỏ sót
			for char in db_characters:
				if char.alias and char.alias not in known_names:
					known_names.append(char.alias)

		detected_list = []
		scene_text_lower = scene_text.lower()

		# 2. THUẬT TOÁN SO KHỚP TÊN (STRING MATCHING PIPELINE) THEO ĐẶC TẢ CHATGPT
		for name in known_names:
			# Nếu tên nhân vật xuất hiện trong văn bản phân cảnh
			if name.lower() in scene_text_lower:
				detected_list.append(name)

		# Nếu cảnh quay không chứa bất kỳ cái tên nào trong thư viện, gán một nhân vật mặc định
		if not detected_list:
			detected_list.append("Default Character")

		# Đóng gói xuất dữ liệu định dạng JSON/Dict sạch theo đúng chuẩn v1.0
		output_json = {
			"characters": detected_list
		}
		
		studio_logger.logger.info(f"Rule-based Detector: Đã so khớp tự động thành công nhân vật: {detected_list}")
		return output_json
