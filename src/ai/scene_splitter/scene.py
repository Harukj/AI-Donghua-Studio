from dataclasses import dataclass, field

@dataclass
class SceneObject:
	"""
	[SCENE DATACLASS COMMERCIAL v1.0]
	Mô hình đối tượng phân cảnh nâng cao sử dụng Dataclass theo đặc tả của ChatGPT.
	Tự động đóng gói thuộc tính điện ảnh sạch cho hệ thống Pipeline.
	"""
	id: str
	chapter: int
	title: str
	summary: str
	
	# Khởi tạo giá trị mặc định dạng danh sách rỗng (field factory list)
	characters: list[str] = field(default_factory=list)
	environments: list[str] = field(default_factory=list)
	props: list[str] = field(default_factory=list)
	
	# Các thuộc tính cảm xúc, máy quay, thời lượng và chuỗi prompt
	mood: str = ""
	camera: str = ""
	duration: float = 0.0
	prompt: str = ""
