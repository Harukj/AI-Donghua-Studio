from sqlalchemy.orm import Session
from database.models.shot import ShotModel
from core.logger import studio_logger

class PromptComposerService:
	def __init__(self, db_session: Session):
		"""Khởi tạo Bộ trộn câu lệnh ma trận 9 lớp - Prompt Composer Service v1.0"""
		self.db = db_session

	def compose_shot_prompt_from_components(self, shot_id: int, dynamic_overrides: dict = None) -> dict:
		"""
		[PROMPT COMPOSER - 9-LAYER STATIC MATRIX FORMULA]
		Tự động bóc tách và xếp chồng 9 lớp thành phần Token theo đúng đặc tả của ChatGPT.
		Tự động cập nhật lan truyền khi các tham số Component đơn lẻ thay đổi.
		"""
		studio_logger.logger.info(f"[PROMPT COMPOSER] Đang nạp ma trận Token 9 lớp cho Shot ID: [{shot_id}]")
		
		# 1. Khởi tạo cấu hình bộ 9 thành phần gốc mặc định khớp 100% hình ảnh trình duyệt
		components = {
			"character": "character profile: to moc, flawless cinematic 3d render",
			"environment": "inside long dang academy ancient courtyard",
			"camera": "close up shot, shallow depth of field",
			"lighting": "volumetric morning light, cinematic golden hour sun rays",
			"weather": "gentle wind blowing, floating atmosphere particles",
			"emotion": "facial expression of calm and focused determination",
			"action": "walking forward slowly, stepping through the main gate",
			"style": "3d chinese donghua animation style",
			"quality": "unreal engine 5 render, ray tracing, masterpiece, crisp details, 16:9 aspect ratio",
			"negative": "low quality, blurry, 2d style, sketch, anime, text, watermark, deformed legs"
		}

		# 2. Áp dụng cơ chế cập nhật tự động (Dynamic Overrides) khi đạo diễn thay đổi Preset góc máy
		if dynamic_overrides:
			for key, val in dynamic_overrides.items():
				if key in components:
					components[key] = val
					studio_logger.logger.info(f" -> [✓] Component '{key.upper()}' tự động cập nhật -> '{val}'")

		# 3. Lắp ráp cơ học trục dọc theo đúng công thức ma trận của ChatGPT
		ordered_matrix = [
			components["style"],
			components["camera"],
			components["character"],
			components["environment"],
			components["lighting"],
			components["weather"],
			components["emotion"],
			f"action context: {components['action'].strip().lower()}",
			components["quality"]
		]

		# Nối chuỗi cơ học ngăn cách bởi dấu phẩy sạch lề
		positive_prompt = ", ".join([token.strip() for token in ordered_matrix if token])
		
		return {
			"shot_id": shot_id,
			"positive": positive_prompt,
			"negative": components["negative"]
		}
