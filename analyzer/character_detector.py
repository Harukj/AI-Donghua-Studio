import json

class EnvironmentDetector:
	def __init__(self, scene_text: str):
		self.scene_text = scene_text

	def detect_environment(self) -> dict:
		"""
		[ENVIRONMENT DETECTOR JSON OUTPUT]
		Tự động quét văn bản phân cảnh để trích xuất không gian bối cảnh phim dạng cấu trúc JSON
		"""
		text_lower = self.scene_text.lower()
		detected_env = "Default Environment"
		
		# Thuật toán quét và nhận diện từ khóa không gian địa điểm điện ảnh
		if "long dạng" in text_lower or "long dang" in text_lower:
			detected_env = "Học viện Long Dạng"
		elif "mạng ước mơ" in text_lower or "dream net" in text_lower:
			detected_env = "Mạng Ước Mơ"
		elif "ký túc xá" in text_lower or "dormitory" in text_lower:
			detected_env = "Ký túc xá"
		elif "đấu trường" in text_lower or "arena" in text_lower:
			detected_env = "Đấu trường"
		elif "học viện" in text_lower or "lớp học" in text_lower:
			detected_env = "Học viện"
			
		# Trả về cấu trúc dữ liệu Dictionary khớp hoàn toàn với chuỗi JSON bối cảnh không gian của ChatGPT
		return {
			"environment": detected_env
		}
