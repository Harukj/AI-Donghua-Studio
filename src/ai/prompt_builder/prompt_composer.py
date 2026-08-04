from src.core.logger import studio_logger

class PromptComposer:
	def __init__(self):
		"""Khởi tạo cỗ máy trộn câu lệnh ma trận 8 lớp - Prompt Composer v1.0"""
		pass

	def compose_matrix_prompt_formula(self, shot_data: dict) -> dict:
		"""
		[MODULE 3 - PROMPT COMPOSER MATRICES]
		Nối chuỗi tĩnh cơ học tuyệt đối dựa theo đúng công thức 8 phân lớp của ChatGPT.
		Triệt tiêu hoàn toàn việc lưu câu lệnh thô cố định trong cơ sở dữ liệu.
		"""
		studio_logger.logger.info(f"[PROMPT COMPOSER] Đang áp dụng công thức ma trận gộp Token cho Cú máy...")

		# Trích xuất bộ 8 phân lớp thông tin từ gói thuộc tính đầu vào
		style = shot_data.get("style", "3D Chinese Donghua animation style, flawless 3D render")
		character = shot_data.get("character", "character portrait info")
		environment = shot_data.get("environment", "inside long dang academy building")
		camera = shot_data.get("camera", "wide shot, shot on 24mm lens")
		lighting = shot_data.get("lighting", "volumetric morning lighting, cinematic sun rays")
		fx = shot_data.get("fx", "floating dust particles, gentle wind blowing")
		action = shot_data.get("action", "walking forward calmly")
		quality = shot_data.get("quality", "unreal engine 5 render, ray tracing, masterpiece, 8k resolution")
		
		negative = shot_data.get("negative", "low quality, blurry, 2d style, sketch, anime, text, watermark")

		# Lắp ráp tuần tự 8 tầng thông tin chặt chẽ cách nhau bằng dấu phẩy
		formula_matrix = [style, camera, character, environment, lighting, fx, f"action: {action.strip().lower()}", quality]
		positive_prompt = ", ".join([tags.strip() for tags in formula_matrix if tags])

		return {
			"positive": positive_prompt,
			"negative": negative,
			"formula_layers_count": len(formula_matrix)
		}
