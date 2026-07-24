import re

class DialogueDetector:
	def __init__(self, scene_text: str):
		"""Khởi tạo với văn bản phân cảnh thô chứa lời thoại"""
		self.scene_text = scene_text

	def extract_dialogues(self) -> dict:
		"""
		[DIALOGUE DETECTOR JSON OUTPUT]
		Tự động bóc tách lời thoại và phân tích ngữ cảnh để tìm ra danh tính người nói.
		Trả về cấu trúc Dictionary tương thích 100% với JSON của ChatGPT.
		"""
		# Phân tách văn bản thành các dòng riêng biệt để phân tích từng dòng một
		lines = [line.strip() for line in self.scene_text.split("\n") if line.strip()]
		
		speaker = "Unknown"
		dialogue_content = ""

		# 1. Thuật toán tìm nội dung câu thoại nằm trong dấu ngoặc kép ""
		for line in lines:
			match_quote = re.search(r'["“]([^"”]*)[["”]', line)
			if match_quote:
				dialogue_content = match_quote.group(1).strip()
				break # Tìm thấy câu thoại đầu tiên trong cảnh thì dừng lại để bóc tách cặp thoại

		# 2. Thuật toán phân tích ngữ cảnh dòng liền kề để tìm người nói (Speaker)
		# Quét danh sách các nhân vật thương mại quen thuộc trong dự án
		known_characters = ["Lâm Uyển", "Tô Mộc", "Lâm Thanh", "Triệu Phong"]
		
		for line in lines:
			# Nếu dòng văn bản chứa tên nhân vật và các từ khóa hành động nói (gọi, nói, hét, thầm...)
			if any(keyword in line for keyword in ["gọi", "nói", "hét", "quát", "lẩm bẩm", "nghĩ"]):
				for char in known_characters:
					if char in line:
						speaker = char
						break

		# Trả về định dạng cấu trúc Dictionary chuẩn xác theo đúng sơ đồ trên ảnh
		return {
			"speaker": speaker,
			"dialogue": dialogue_content
		}
