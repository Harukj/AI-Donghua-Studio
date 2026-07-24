from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ShotObject:
	"""
	[SHOT DATACLASS OBJECT COMMERCIAL STANDARD]
	Mô hình đối tượng cú máy điện ảnh ảo v1.0 theo đặc tả của ChatGPT.
	Đóng gói khép kín toàn bộ 12 thuộc tính cinematic phục vụ dây chuyền sản xuất phim.
	"""
	id: int
	scene_id: int
	index: int
	
	camera: str = "Medium Shot"
	lens: str = "Standard 50mm"
	movement: str = "Static"
	duration: float = 3.0
	lighting: str = "Morning"
	seed: str = ""
	
	prompt: str = ""
	video_path: str = ""
	status: str = "waiting"
	created_at: datetime = field(default_factory=datetime.utcnow)

	def __repr__(self) -> str:
		return f"<ShotObject [ID: {self.id}] Scene_ID: {self.scene_id} Index: {self.index} Status: {self.status}>"
