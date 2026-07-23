class EnvironmentDetector:
	def __init__(self, scene_text: str):
		self.scene_text = scene_text

	def detect_environment(self) -> str:
		"""Tự động quét văn bản để trích xuất không gian bối cảnh phim"""
		text_lower = self.scene_text.lower()
		if "thành phố" in text_lower or "mái nhà" in text_lower:
			return "Long Dang City"
		if "học viện" in text_lower or "lớp học" in text_lower:
			return "Academy"
		return "Default Environment"
