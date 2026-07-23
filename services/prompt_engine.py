from sqlalchemy.orm import Session
from database.models.camera import CameraModel

class PromptEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo engine kết nối cơ sở dữ liệu SQLite"""
		self.db = db_session

	def get_camera_prompt(self, camera_name: str) -> str:
		"""Truy vấn chính xác từ khóa cấu hình của góc máy từ Thư viện Camera"""
		camera = self.db.query(CameraModel).filter(CameraModel.name == camera_name).first()
		if camera:
			return camera.camera_prompt
		return f"{camera_name.lower()} shot"

	def generate_from_scene_object(self, scene, default_lighting: str = "Golden Hour", default_mood: str = "Epic") -> str:
		"""
		[PROMPT ENGINE v1.0 - STATIC MIXER CORES]
		Ủy quyền ép chuỗi cơ học: KHÔNG CHO AI TỰ VIẾT PROMPT.
		Gom 5 thành phần sạch từ Database để tạo cấu trúc câu lệnh điện ảnh đồng nhất 100%.
		"""
		# 1. THÀNH PHẦN 1: CHARACTER BIBLE (Lấy mảng danh sách tên nhân vật)
		characters_part = ", ".join(scene.characters) if hasattr(scene, 'characters') and scene.characters else "Default Character"
		
		# 2. THÀNH PHẦN 2: ENVIRONMENT LIBRARY (Lấy không gian bối cảnh mẫu)
		environments_part = ", ".join(scene.environments) if hasattr(scene, 'environments') and scene.environments else "Default Environment"
		
		# 3. THÀNH PHẦN 3: CAMERA (Góc máy điện ảnh cố định từ thư viện)
		camera_name = "Wide Shot" # Hoặc trích xuất từ cấu hình scene.camera nếu có
		camera_prompt = self.get_camera_prompt(camera_name)
		
		# 4. THÀNH PHẦN 4: LIGHTING (Bộ lọc ánh sáng nghệ thuật cố định)
		lighting_prompt = f"{default_lighting.lower()} lighting"
		
		# 5. THÀNH PHẦN 5: MOOD (Bầu không khí / Sắc thái cảm xúc của phân cảnh)
		mood_prompt = f"{default_mood.lower()} atmosphere"

		# TIẾN HÀNH GHÉP PROMPT CƠ HỌC (STATIC CONCATENATION) THEO ĐÚNG SƠ ĐỒ CHATGPT
		# Cấu trúc chuỗi được kiểm soát chặt chẽ, tối ưu cấu trúc Token cho mô hình AI LTX Studio
		prompt_elements = [
			"masterpiece",
			"Chinese Donghua style",
			camera_prompt,
			f"character {characters_part}",
			f"standing in {environments_part}",
			lighting_prompt,
			mood_prompt,
			"cinematic composition",
			"ultra detailed texture",
			"16:9 aspect ratio"
		]
		
		# Lọc sạch các khoảng trống và nối lại với nhau bằng dấu phẩy
		final_ltx_prompt = ", ".join([element.strip() for element in prompt_elements if element])
		return final_ltx_prompt
