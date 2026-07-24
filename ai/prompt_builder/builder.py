import os
from ai.prompt_builder.templates_manager import TemplateManager
from core.logger import studio_logger

class StaticPromptBuilder:
	def __init__(self):
		"""Khởi tạo bộ trộn câu lệnh, tiêm phụ thuộc bộ quản lý TemplateManager"""
		self.template_mgr = TemplateManager()

	def generate_prompt_from_scene(self, scene_obj, template_name: str = "ltx_default", camera_key: str = "wide", lighting_key: str = "morning") -> dict:
		"""
		[PROMPT BUILDER CORE LOGIC]
		Đọc trực tiếp dữ liệu từ thực thể Scene Object sạch và thay thế vào Template cứng.
		Xuất ra cấu trúc câu lệnh gồm cả trường Positive và Negative chuẩn chỉ cho Render Queue.
		"""
		# 1. Gọi bộ quản lý nạp file template nghệ thuật được chọn
		config = self.template_mgr.load_template_config(template_name)
		
		# 2. Trích xuất bộ 5 lớp thông tin điện ảnh cơ học trực tiếp từ thực thể Scene Object
		character_part = ", ".join(scene_obj.characters) if scene_obj.characters else "Tô Mộc"
		environment_part = ", ".join(scene_obj.environments) if scene_obj.environments else "Học viện"
		action_part = scene_obj.summary if scene_obj.summary else ""
		mood_part = getattr(scene_obj, 'mood', 'Epic')

		# 3. Trích xuất từ khóa cinematic cố định từ file JSON cấu hình
		style_part = config.get("style", "3D Donghua style")
		camera_part = config.get("camera_presets", {}).get(camera_key, "medium shot")
		lighting_part = config.get("lighting_presets", {}).get(lighting_key, "soft lighting")
		negative_prompt = config.get("negative", "")

		# 4. TIẾN HÀNH LẮP GHÉP THEO ĐÚNG TEMPLATE KHAI BÁO BIẾN CỦA CHATGPT
		positive_components = [
			style_part,
			camera_part,
			f"character {character_part}",
			f"location inside {environment_part.lower()}",
			lighting_part,
			f"{mood_atmosphere.lower()} mood" if 'mood_atmosphere' in locals() else f"{mood_part.lower()} atmosphere",
			f"action {action_part.lower()}" if action_part else ""
		]
		
		positive_prompt = ", ".join([tags.strip() for tags in positive_components if tags])
		
		studio_logger.logger.info(f"Prompt Builder: Đã sinh cặp Prompt sạch cho phân cảnh [{scene_obj.id}]")
		
		# Trả về gói kết quả sẵn sàng cấp cho cỗ máy render
		return {
			"positive": positive_prompt,
			"negative": negative_prompt
		}
