from dataclasses import dataclass

@dataclass
class Shot:
	"""
	[SHOT OBJECT COMMERCIAL STANDARD]
	Class định nghĩa cấu trúc một cú máy điện ảnh ảo theo đặc tả v0.6 của ChatGPT.
	Ép kiểu dữ liệu nghiêm ngặt để tối ưu hóa token truyền dữ liệu cho hàng đợi Render.
	"""
	id: int
	scene_id: int
	index: int
	camera: str
	lens: str
	movement: str
	duration: float
	lighting: str
	seed: str
	prompt: str
	video_path: str
