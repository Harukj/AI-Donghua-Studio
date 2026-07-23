from sqlalchemy.orm import Session
from database.models.camera import CameraModel

class PromptEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo engine kết nối cơ sở dữ liệu SQLite"""
		self.db = db_session

	def get_camera_prompt(self, camera_name: str) -> str:
		"""Truy vấn từ khóa cấu hình của góc máy từ Thư viện Camera"""
		camera = self.db.query(CameraModel).filter(CameraModel.name == camera_name).first()
		if camera:
			return camera.camera_prompt
		return f"{camera_name.lower()} shot"

	def generate_from_scene_object(self, scene) -> str:
		"""
		[PROMPT ENGINE v1.0 - STATIC MIXER CORES]
		Ép chuỗi cơ học: KHÔNG CHO PROMPT ENGINE ĐỌC DOCX.
		Chỉ đọc thực thể Scene Object để tạo cấu trúc câu lệnh điện ảnh đồng nhất 100%.
		"""
		# 1. THÀNH PHẦN 1: CHARACTER (Lấy nhân vật từ thuộc tính đối tượng)
		character_part = scene.characters if hasattr(scene, 'characters') and scene.characters else "Tô Mộc"
		if isinstance(character_part, list):
			character_part = ", ".join(character_part)
		
		# 2. THÀNH PHẦN 2: ENVIRONMENT (Lấy bối cảnh không gian)
		environment_part = scene.environments if hasattr(scene, 'environments') and scene.environments else "Ký túc xá"
		if isinstance(environment_part, list):
			environment_part = ", ".join(environment_part)
		
		# 3. THÀNH PHẦN 3: CAMERA (Góc máy điện ảnh cố định từ thuộc tính đối tượng)
		camera_name = scene.camera if hasattr(scene, 'camera') and scene.camera else "Wide Shot"
		camera_prompt = self.get_camera_prompt(camera_name)
		
		# 4. THÀNH PHẦN 4: LIGHTING (Bộ lọc ánh sáng nghệ thuật lấy từ đối tượng)
		lighting_name = scene.mood if hasattr(scene, 'mood') and scene.mood else "Morning"
		lighting_prompt = f"{lighting_name.lower()} lighting"

		# TIẾN HÀNH GHÉP PROMPT CƠ HỌC (STATIC CONCATENATION) THEO ĐÚNG SƠ ĐỒ CHATGPT
		prompt_elements = [
			"masterpiece",
			"Chinese Donghua style",
			camera_prompt,
			f"character {character_part}",
			f"inside {environment_part.lower()}",
			lighting_prompt,
			"cinematic composition",
			"ultra detailed texture",
			"16:9 aspect ratio"
		]
		
		# Lọc sạch các khoảng trống và nối lại với nhau bằng dấu phẩy
		final_ltx_prompt = ", ".join([element.strip() for element in prompt_elements if element])
		return final_ltx_prompt
