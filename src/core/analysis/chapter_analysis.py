class ChapterAnalysis:
	def __init__(self, raw_text: str):
		self.raw_text = raw_text

	def analyze_structure(self) -> dict:
		"""
		Phân tích cấu trúc thô của chương truyện: 
		Đếm số từ, ước tính thời lượng phim và phát hiện từ khóa hành động.
		"""
		words = self.raw_text.split()
		word_count = len(words)
		
		# Giả lập công thức điện ảnh: Trung bình 150 từ truyện chữ sẽ chuyển hóa thành 1 phút phim hoạt hình 3D
		estimated_duration_minutes = round(word_count / 150, 2)
		
		# Quét nhanh mật độ từ khóa cao trào/hành động để gán sắc thái phân cảnh
		action_keywords = ["đấu", "chém", "bộc phát", "gầm lên", "vỡ vụn", "thần thông"]
		intensity_score = sum(1 for word in words if any(kw in word.lower() for kw in action_keywords))
		
		return {
			"word_color": word_count,
			"estimated_duration_minutes": estimated_duration_minutes,
			"intensity_score": intensity_score,
			"status": "Ready for Scene Splitting"
		}
