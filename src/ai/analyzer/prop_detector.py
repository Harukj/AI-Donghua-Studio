class PropDetector:
	def __init__(self, scene_text: str):
		self.scene_text = scene_text

	def detect_props(self) -> list[str]:
		"""Tự động quét văn bản để trích xuất vũ khí, pháp bảo hoặc vật phẩm cầm tay"""
		detected_props = []
		text_lower = self.scene_text.lower()
		if "kiếm" in text_lower: detected_props.append("Kiếm")
		if "bảo vật" in text_lower: detected_props.append("Bảo vật")
		return detected_props if detected_props else ["None"]
