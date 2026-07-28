from core.logger import studio_logger

class PromptTemplateEngine:
	def __init__(self):
		"""Khởi tạo Bộ quản lý mẫu câu lệnh - Prompt Template Engine v1.0 (Coding Standard)"""
		# Khởi tạo các mẫu Preset Token điện ảnh sạch ghim cứng trong mã nguồn thay cho biến Global
		self._style_presets = {
			"donghua_3d": "3D Chinese Donghua animation style, flawless cinematic 3D render, Unreal Engine 5",
			"cyberpunk": "Cinematic cyberpunk donghua animation style, neon lighting, highly detailed 3D"
		}

	def compile_cinematic_template(self, template_key: str, character_token: str, environment_token: str) -> str:
		"""
		[CODING STANDARD - TEMPLATE LAYER]
		Nạp động cấu trúc mẫu câu lệnh và thực hiện biên dịch Token sạch.
		Triệt tiêu hoàn toàn việc viết cứng Prompt thô trong tầng giao diện người dùng GUI.
		"""
		selected_style = self._style_presets.get(template_key.lower().strip(), self._style_presets["donghua_3d"])
		
		# Xếp chồng ma trận 3 lớp thành phần cơ học sạch lề bám sát triết lý Component
		compiled_prompt = f"{selected_style}, character: {character_token.strip()}, setting: {environment_token.strip()}"
		
		studio_logger.logger.info(f"[PROMPT TEMPLATE] Đã biên dịch thành công mẫu câu lệnh [Key: {template_key.upper()}]")
		return compiled_prompt
