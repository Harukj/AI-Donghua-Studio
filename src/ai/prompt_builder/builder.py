import os
from src.ai.prompt_builder.templates_manager import TemplateManager
from src.core.logger import studio_logger

class StaticPromptBuilder:
	def __init__(self):
		"""Khởi tạo bộ trộn câu lệnh điện ảnh, nạp bộ quản lý mẫu"""
		self.template_mgr = TemplateManager()

	def generate_prompt_from_scene(self, scene_obj) -> dict:
		"""
		[CONTEXT-AWARE PROMPT MIXER]
		Tự động nhận diện ngữ cảnh phân cảnh để chọn đúng tệp cấu hình:
		Chứa lời thoại -> ltx_dialogue | Chứa hành động mạnh -> ltx_action | Mặc định -> ltx_cinematic.
		"""
		action_text = scene_obj.summary.lower() if scene_obj.summary else ""
		
		# 1. THUẬT TOÁN ĐIỀU PHỐI CHỌN TEMPLATE THEO ĐẶC TẢ CỦA CHATGPT
		template_name = "ltx_cinematic" # Mặc định chọn mẫu toàn cảnh điện ảnh
		camera_key = "establishing"
		lighting_key = "volumetric"
		
		# Nếu phân cảnh xuất hiện mảng lời thoại kịch bản
		if hasattr(scene_obj, 'dialogues') and scene_obj.dialogues and len(scene_obj.dialogues) > 0:
			template_name = "ltx_dialogue"
			camera_key = "dialogue"
			lighting_key = "interior"
		# Nếu phân cảnh chứa từ khóa va chạm kịch tính, chiến đấu
		elif any(kw in action_text for kw in ["đấu", "chém", "lao vào", "oanh", "ầm ầm", "vèo", "đấm"]):
			template_name = "ltx_action"
			camera_key = "combat"
			lighting_key = "dramatic"

		# 2. Nạp file cấu hình JSON tương ứng từ bộ quản lý
		config = self.template_mgr.load_template_config(template_name)
		
		# 3. Trích xuất thực thể sạch hướng đối tượng từ Scene Object
		character_part = ", ".join(scene_obj.characters) if scene_obj.characters else "Tô Mộc"
		environment_part = ", ".join(scene_obj.environments) if scene_obj.environments else "Học viện Long Dạng"
		mood_part = getattr(scene_obj, 'mood', 'Epic')

		# 4. Lấy từ khóa cinematic cố định từ cấu hình tệp nạp được
		style_part = config.get("style", "Chinese Donghua style")
		camera_part = config.get("camera_presets", {}).get(camera_key, "cinematic shot")
		lighting_part = config.get("lighting_presets", {}).get(lighting_key, "cinematic lighting")
		negative_prompt = config.get("negative", "")

		# 5. LẮP GHÉP CƠ HỌC CHUỖI TOKEN ĐỒNG NHẤT 100%
		positive_components = [
			style_part,
			camera_part,
			f"character {character_part}",
			f"scene setting inside {environment_part.lower()}",
			lighting_part,
			f"{mood_part.lower()} atmosphere",
			f"action scene description: {scene_obj.summary.lower()}" if scene_obj.summary else ""
		]
		
		positive_prompt = ", ".join([tags.strip() for tags in positive_components if tags])
		
		studio_logger.logger.info(f"Prompt Builder: Đã áp dụng mẫu [{template_name}] tự động cho [{scene_obj.id}]")
		
		return {
			"positive": positive_prompt,
			"negative": negative_prompt
		}
