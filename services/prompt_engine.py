from sqlalchemy.orm import Session
from analyzer.scene_object import Scene
from database.models.camera import CameraModel

class PromptEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo engine kết nối với phiên làm việc dữ liệu SQLite"""
		self.db = db_session

	def get_camera_prompt(self, camera_name: str) -> str:
		"""Truy vấn từ khóa cấu hình của góc máy từ thư viện máy quay"""
		camera = self.db.query(CameraModel).filter(CameraModel.name == camera_name).first()
		if camera:
			return camera.camera_prompt
		return f"{camera_name.lower()} shot"

	def generate_from_scene_object(self, scene: Scene, default_lighting: str = "Golden Hour", default_mood: str = "Epic") -> str:
		"""
		[PROMPT ENGINE v1.0 ARCHITECTURE]
		Hàm nhận đầu vào duy nhất là thực thể Class Scene Object sạch.
		Tự động bóc tách mảng thuộc tính và trộn thành câu lệnh LTX Prompt thương mại hoàn chỉnh.
		"""
		# 1. Trích xuất danh sách nhân vật và bối cảnh từ thuộc tính đối tượng Object
		# Sử dụng dấu phẩy để nối chuỗi nếu phân cảnh xuất hiện nhiều thực thể
		characters_part = ", ".join(scene.characters) if scene.characters else "Default Character"
		environments_part = ", ".join(scene.environments) if scene.environments else "Default Environment"
		
		# 2. Xử lý trích xuất danh sách vật phẩm/vũ khí (Props) từ Object
		props_part = f"holding {', '.join(scene.props).lower()}" if scene.props and "none" not in [p.lower() for p in scene.props] else ""

		# 3. Lấy thông số góc máy điện ảnh mặc định
		# Nếu danh sách phân cảnh chưa có cấu hình góc máy, mặc định sử dụng Medium Shot
		camera_name = "Medium Shot"
		camera_prompt = self.get_camera_prompt(camera_name)
		
		# 4. Thiết lập bộ lọc nghệ thuật nâng cao (Ánh sáng & Bầu không khí cảm xúc)
		lighting_prompt = f"{default_lighting.lower()} lighting"
		mood_prompt = f"{default_mood.lower()} mood"
		
		# 5. Tiến hành lắp ráp chuỗi Mixer điện ảnh theo đúng sơ đồ luồng v1.0 của ChatGPT
		# Cấu trúc chuỗi: Phong cách hoạt hình gốc, Góc máy, Nhân vật, Vũ khí, Bối cảnh không gian, Ánh sáng, Cảm xúc cảnh
		prompt_elements = [
			"Chinese Donghua style",
			camera_prompt,
			characters_part,
			props_part,
			f"in {environments_part}",
			lighting_prompt,
			mood_prompt,
			"masterpiece",
			"cinematic composition",
			"16:9 aspect ratio"
		]
		
		# Lọc bỏ các chuỗi rỗng và nối lại một cách sạch sẽ bằng dấu phẩy
		ltx_prompt = ", ".join([element.strip() for element in prompt_elements if element])
		return ltx_prompt
