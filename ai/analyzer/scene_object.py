class Scene:
	def __init__(
		self,
		id: str,
		chapter: int,
		title: str,
		summary: str,
		characters: list,
		environments: list,
		props: list,
		dialogues: list,
		duration: float
	):
		"""
		[SCENE OBJECT COMMERCIAL STANDARD]
		Class định nghĩa cấu trúc một phân cảnh điện ảnh chuẩn v1.0.
		Thay thế hoàn toàn cho việc dùng Dict lỏng lẻo trước đây.
		"""
		self.id = id                      # Định danh phân cảnh (Ví dụ: "SCENE_01")
		self.chapter = chapter            # Số thứ tự chương truyện (Kiểu số nguyên: int)
		self.title = title                # Tiêu đề/Tên phân cảnh ngắn gọn
		self.summary = summary            # Tóm tắt kịch bản nội dung phân cảnh
		self.characters = characters      # Danh sách mảng chứa các nhân vật xuất hiện (list)
		self.environments = environments  # Danh sách mảng chứa các không gian bối cảnh (list)
		self.props = props                # Danh sách mảng chứa vũ khí, pháp bảo (list)
		self.dialogues = dialogues        # Danh sách mảng chứa các câu thoại (list)
		self.duration = duration          # Thời lượng ước tính sinh phân cảnh phim (float)

	def __repr__(self) -> str:
		return f"<Scene Object [ID: {self.id}] Characters: {self.characters}>"
