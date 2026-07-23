from core.logger import studio_logger

class AdvancedSceneSplitter:
	def __init__(self, chapter_content: str):
		"""Khởi tạo bộ tách phân cảnh nâng cao với nội dung một chương truyện"""
		self.raw_text = chapter_content.strip()

	def execute_split(self) -> list[str]:
		"""
		[SPRINT 6 - LINE-LEVEL SPLITTING ALGORITHM]
		Tự động bẻ tách chương truyện dựa trên dấu chấm ngắt câu và đoạn văn hành động.
		Đảm bảo trích xuất ra các Scene độc lập như đặc tả của ChatGPT.
		"""
		studio_logger.logger.info("Scene Splitter: Đang thực thi bẻ cảnh theo đặc tả Sprint 6...")
		
		# Tách văn bản thô theo từng dòng hoặc dấu chấm câu lớn để bắt hành động ngắn
		lines = [line.strip() for line in self.raw_text.split("\n") if line.strip()]
		
		final_scenes = []
		for line in lines:
			# Xử lý bẻ nhỏ hơn nếu một dòng chứa nhiều câu độc lập cách nhau bằng dấu chấm
			sub_sentences = [s.strip() for s in line.split(".") if s.strip()]
			for sentence in sub_sentences:
				# Giữ lại nội dung câu văn hành động sạch làm cốt lõi phân cảnh
				final_scenes.append(f"{sentence}.")

		studio_logger.logger.info(f"Scene Splitter: Hoàn thành. Đã bẻ tách thành công {len(final_scenes)} phân cảnh mẫu.")
		return final_scenes
