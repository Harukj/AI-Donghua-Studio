class ChapterAnalyzer:
	def __init__(self, raw_text: str):
		self.raw_text = raw_text

	def analyze(self) -> dict:
		"""Bóc tách và ước lượng thông số thời lượng tổng quan của chương truyện"""
		words = self.raw_text.split()
		return {
			"word_count": len(words),
			"estimated_minutes": round(len(words) / 150, 2),
			"status": "Success"
		}
