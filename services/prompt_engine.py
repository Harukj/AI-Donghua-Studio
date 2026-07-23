from sqlalchemy.orm import Session
from services.character_service import CharacterService
from services.environment_service import EnvironmentService
from database.models.camera import CameraModel

class PromptEngine:
	def __init__(self, db_session: Session):
		self.db = db_session
		self.char_service = CharacterService(db_session)
		self.env_service = EnvironmentService(db_session)

	def get_camera_prompt(self, camera_name: str) -> str:
		camera = self.db.query(CameraModel).filter(CameraModel.name == camera_name).first()
		if camera:
			return camera.camera_prompt
		return f"{camera_name.lower()} shot"

	def generate_scene_prompt(self, character_name: str, env_name: str, camera_name: str, lighting: str = "Golden Hour", mood: str = "Epic") -> dict:
		"""
		[PROMPT ENGINE WITH SEED LOGIC]
		Tự động trộn: Góc máy + Hồ sơ nhân vật + Bối cảnh + Ánh sáng + Cảm xúc.
		Đồng thời bóc tách mã Seed cố định để gửi sang hệ thống sinh video AI.
		"""
		# 1. Trích xuất thông tin hồ sơ nhân vật từ Character Bible
		character = self.char_service.get_character_by_name(character_name)
		char_prompt = self.char_service.build_ai_prompt(character_name)
		
		# Lấy mã seed cố định của nhân vật (nếu không có, mặc định trả về chuỗi trống)
		character_seed = character.seed if character and hasattr(character, 'seed') and character.seed else ""
		
		# 2. Trích xuất thông tin bối cảnh không gian từ Environment Bible
		env_prompt = self.env_service.build_environment_prompt(env_name)
		
		# 3. Lấy thông số góc quay từ Camera Library
		camera_prompt = self.get_camera_prompt(camera_name)
		
		# 4. Thiết lập bộ lọc nghệ thuật bổ trợ
		lighting_prompt = f"{lighting.lower()} lighting" if lighting else ""
		mood_prompt = f"{mood.lower()} mood" if mood else ""
		
		# 5. Tiến hành lắp ráp chuỗi LTX Prompt hoàn chỉnh theo đúng cấu trúc điện ảnh
		prompt_elements = [
			camera_prompt,
			char_prompt,
			f"in {env_prompt}",
			lighting_prompt,
			mood_prompt
		]
		
		ltx_prompt = ", ".join([element.strip() for element in prompt_elements if element])
		
		# Trả về một Dictionary chứa cả chuỗi câu lệnh lẫn mã seed để nạp cho mô hình AI
		return {
			"prompt": ltx_prompt,
			"seed": character_seed
		}
