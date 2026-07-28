from sqlalchemy.orm import Session
from ai.prompt_builder.prompt_template import PromptTemplateEngine
from core.logger import studio_logger

class PromptService:
	def __init__(self, db_session: Session):
		"""
		[PROMPT SERVICE MATRIX ENGINE v1.0]
		Tích hợp toàn vẹn giữa bộ trộn ma trận 9 lớp cũ và bộ quản lý Template sạch mới.
		Triệt tiêu hoàn toàn lỗi AttributeError và xung đột luồng nạp hệ thống.
		"""
		self.db = db_session
		self.template_loader = PromptTemplateEngine()

	def generate_packaged_shot_prompt(self, template_type: str, character_name: str, location_name: str) -> dict:
		"""Luồng sinh Prompt sạch bám sát Coding Standard v1.0"""
		studio_logger.logger.info("[PROMPT SERVICE] Biên dịch Prompt thông qua lớp Template...")
		positive_string = self.template_loader.compile_cinematic_template(
			template_key=template_type,
			character_token=character_name,
			environment_token=location_name
		)
		return {
			"status": "compiled",
			"prompt_payload": {
				"positive": positive_string,
				"negative": "low quality, blurry, 2d style, sketch, deformed body, text, watermark"
			}
		}

	def compose_shot_prompt_from_components(self, shot_id: int, dynamic_overrides: dict = None) -> dict:
		"""
		[VÁ LỖI ATTRIBUTEERROR - BACKWARD COMPATIBILITY LUỒNG TỰ TRỊ]
		Khôi phục chính xác 100% thuật toán trộn ma trận 9 lớp phục vụ cho AI Production Assistant.
		"""
		studio_logger.logger.info(f"[PROMPT CORES] Đang thực thi trộn ma trận Token 9 lớp cho Shot ID: [{shot_id}]")
		
		components = {
			"style": "3d chinese donghua animation style",
			"camera": "close up shot, shallow depth of field",
			"character": "character profile: to moc, flawless cinematic 3d render",
			"environment": "inside long dang academy ancient courtyard",
			"lighting": "volumetric morning light, cinematic golden hour sun rays",
			"weather": "gentle wind blowing, floating atmosphere particles",
			"emotion": "facial expression of calm and focused determination",
			"action": "walking forward slowly",
			"quality": "unreal engine 5 render, ray tracing, masterpiece, crisp details",
			"negative": "low quality, blurry, 2d style, sketch, anime, text, watermark"
		}

		if dynamic_overrides:
			for key, val in dynamic_overrides.items():
				if key in components:
					components[key] = val

		ordered_matrix = [
			components["style"], components["camera"], components["character"],
			components["environment"], components["lighting"], components["weather"],
			components["emotion"], f"action context: {components['action'].strip().lower()}",
			components["quality"]
		]

		positive_prompt = ", ".join([token.strip() for token in ordered_matrix if token])
		
		return {
			"shot_id": shot_id,
			"positive": positive_prompt,
			"negative": components["negative"]
		}

# Ghép bí danh đóng băng hệ thống để giữ kết nối với các import cũ
PromptComposerService = PromptService
