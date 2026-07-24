from sqlalchemy.orm import Session
from services.character_service import CharacterService
from services.environment_service import EnvironmentService
from core.logger import studio_logger

class PromptBuilder30:
	def __init__(self, db_session: Session):
		"""Khởi tạo cỗ máy ma trận Prompt Builder 3.0 kết nối dữ liệu"""
		self.db = db_session
		self.char_service = CharacterService(db_session)
		self.env_service = EnvironmentService(db_session)

	def build_matrix_prompt_v3(self, char_name: str, location_name: str, raw_action_text: str, directives: dict) -> dict:
		"""
		[PROMPT BUILDER 3.0 - DYNAMIC CONTEXT MIXER]
		Tự động bóc tách 6 tầng thông số nghệ thuật thực tế từ AI Director 
		kết hợp tài nguyên hồ sơ cấu trúc sạch từ Character/Environment Bible.
		"""
		studio_logger.logger.info("[DREAMFORGE ENGINE] Ma trận 3.0 đang lắp ráp câu lệnh từ chỉ đạo của AI Director...")

		# 1. TRÍCH XUẤT TÀI NGUYÊN TỪ DATABASE QUA SERVICES (LỚP 1 & 2)
		character_tags = self.char_service.get_fixed_character_prompt_tags(char_name)
		environment_tags = self.env_service.get_fixed_environment_prompt_tags(location_name)

		# 2. BÓC TÁCH MÔ-ĐUN ĐIỆN ẢNH TỪ GÓI CHỈ THỊ CỦA AI ĐẠO DIỄN (LỚP 3, 4, 5)
		emotion = directives.get("emotion", "surprised")
		camera_shot = directives.get("camera", "close up shot")
		lens = directives.get("lens", "85mm")
		movement = directives.get("movement", "quick pan")
		lighting = directives.get("lighting", "cold light")

		# 3. LẮP RÁP CƠ HỌC 20 MODULES ĐỒNG NHẤT 100% THEO ĐÚNG ĐẶC TẢ CHATGPT
		prompt_template = [
			"3D Chinese Donghua animation style, flawless cinematic 3D render",
			f"{camera_shot.lower()}",
			f"shot with {lens} lens",
			f"{movement.lower()} camera movement",
			f"character {character_tags}",
			f"facial expression of {emotion.lower()}",
			f"inside environment setting {environment_tags.lower()}",
			f"under professional {lighting.lower()} setup",
			f"action: {raw_action_text.strip().lower()}",
			"unreal engine 5 render, ray tracing, masterpiece, crisp details, 16:9 aspect ratio"
		]

		positive_prompt = ", ".join([tags.strip() for tags in prompt_template if tags])
		negative_prompt = "low quality, blurry, 2d style, sketch, anime, text, watermark, deformed lips"

		return {
			"positive": positive_prompt,
			"negative": negative_prompt,
			"duration": directives.get("duration", 3.5)
		}
