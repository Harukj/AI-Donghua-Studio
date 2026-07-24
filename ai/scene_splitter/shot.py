from dataclasses import dataclass

@dataclass
class Shot:
	"""
	[SHOT OBJECT UPGRADED v0.6]
	Class định nghĩa cấu trúc cú máy hoạt hình tích hợp phân lớp ngữ cảnh điện ảnh.
	"""
	id: int
	scene_id: int
	index: int
	context_type: str  # Trường dữ liệu mới: 'establishing', 'action', 'reaction', 'dialogue'
	camera: str
	lens: str
	movement: str
	duration: float
	lighting: str
	seed: str
	prompt: str
	video_path: str
