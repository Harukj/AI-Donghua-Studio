class CharacterDetector:
	def __init__(self, scene_text: str):
		self.scene_text = scene_text

	def detect_characters(self) -> list[str]:
		"""Tự động quét văn bản phân cảnh để nhận diện tên nhân vật xuất hiện"""
		detected = []
		if "Tô Mộc" in self.scene_text: detected.append("Tô Mộc")
		if "Lâm Thanh" in self.scene_text: detected.append("Lâm Thanh")
		return detected if detected else ["Default Character"]
