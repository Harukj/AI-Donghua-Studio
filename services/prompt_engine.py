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

	def generate_from_scene_object(self, scene) -> str:
		"""
		[PROMPT ENGINE UPGRADED WITH AI DIRECTOR]
		Nhận Scene Object -> Gọi Đạo diễn AI tự phân tích -> Trộn prompt điện ảnh tối ưu
		"""
		# Khởi động bộ não Đạo diễn AI độc quyền xử lý kịch bản chữ thô của phân cảnh
		from analyzer.ai_director import AIDirector
		ai_director = AIDirector(scene.summary)
		ai_decisions = ai_director.make_cinematic_decisions()
		
		# Trích xuất các quyết định nghệ thuật tự động từ AI Director
		detected_emotion = ai_decisions["emotion"]
		camera_prompt = ai_decisions["camera"]
		lens_prompt = ai_decisions["lens"]
		lighting_prompt = ai_decisions["lighting"]
		
		# Trích xuất các thực thể cơ bản có sẵn trong Object
		characters_part = ", ".join(scene.characters) if scene.characters else "Default Character"
		environments_part = ", ".join(scene.environments) if scene.environments else "Default Environment"
		props_part = f"holding {', '.join(scene.props).lower()}" if scene.props and "none" not in [p.lower() for p in scene.props] else ""

		# Tiến hành lắp ráp Mixer điện ảnh 5 sao theo chuẩn v1.0 của Studio
		prompt_elements = [
			"Chinese Donghua 3D animation style",
			f"{camera_prompt}",
			f"{lens_prompt}",
			f"character {characters_part} showing {detected_emotion.lower()} emotion",
			props_part,
			f"scene takes place in {environments_part}",
			f"{lighting_prompt}",
			"masterpiece",
			"cinematic composition",
			"highly detailed texture",
			"16:9 cinematic aspect ratio"
		]
		
		return ", ".join([element.strip() for element in prompt_elements if element])
