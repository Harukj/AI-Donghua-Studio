class DialogueDetector:
	def __init__(self, scene_text: str):
		self.scene_text = scene_text

	def extract_dialogues(self) -> list[dict]:
		"""Tự động bóc tách các câu thoại nằm trong dấu ngoặc kép của phân cảnh"""
		import re
		# Tìm các chuỗi văn bản nằm bên trong dấu ngoặc kép ""
		matches = re.findall(r'"([^"]*)"', self.scene_text)
		dialogues = []
		for match in matches:
			dialogues.append({
				"speaker": "Unknown", # Sẽ được AI phân tích người nói ở Sprint sau
				"line": match.strip()
			})
		return dialogues
