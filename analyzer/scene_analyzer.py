class SceneAnalyzer:
	def __init__(self, chapter_text: str):
		self.chapter_text = chapter_text

	def split_scenes(self) -> list[str]:
		"""Bẻ nhỏ nội dung chương truyện chữ thành các phân cảnh hành động độc lập"""
		return [s.strip() for s in self.chapter_text.split("\n\n") if s.strip()]
