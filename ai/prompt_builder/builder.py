import os
import json
from core.logger import studio_logger

class StaticPromptBuilder:
	def __init__(self):
		"""Khởi tạo bộ dựng Prompt dựa trên file cấu hình Template tĩnh"""
		base_path = os.path.dirname(os.path.abspath(__file__))
		template_path = os.path.join(base_path, "templates", "donghua_3d.json")
		
		# Tải bộ từ khóa cấu hình nghệ thuật cố định
		with open(template_path, "r", encoding="utf-8") as f:
			self.templates = json.load(f)

	def build_string_mixer(self, detected_data: dict, camera_key: str = "wide", lighting_key: str = "morning") -> str:
		"""
		[PROMPT BUILDER CONCATENATION PIPELINE]
		Nối chuỗi cơ học các thực thể sạch với bộ khung từ khóa cố định.
		Triệt tiêu hoàn toàn sự ngẫu nhiên hoặc ảo tưởng từ ngữ của AI.
		"""
		# 1. Trích xuất tài nguyên từ bộ quét Rule-based của Sprint trước
		characters = detected_data.get("characters", ["Default Character"])
		environment = detected_data.get("environment", "Default Environment")
		
		char_part = ", ".join(characters)
		
		# 2. Lấy từ khóa điện ảnh cố định từ file Template JSON cấu hình
		style = self.templates.get("style_prefix", "")
		camera = self.templates.get("camera_presets", {}).get(camera_key, "medium shot")
		lighting = self.templates.get("lighting_presets", {}).get(lighting_key, "soft lighting")
		suffix = self.templates.get("quality_suffixes", "")

		# 3. LẮP GHÉP CƠ HỌC THEO ĐÚNG QUY TẮC PHÂN LỚP CỦA KTS PHẦN MỀM CHATGPT
		prompt_components = [
			style,
			camera,
			f"character {char_part}",
			f"inside {environment.lower()}",
			lighting,
			suffix
		]
		
		# Lọc bỏ khoảng trống và nối lại chặt chẽ bằng dấu phẩy
		final_prompt = ", ".join([tags.strip() for tags in prompt_components if tags])
		
		studio_logger.logger.info("Prompt Builder: Đã sinh chuỗi câu lệnh LTX cố định ổn định 100%.")
		return final_prompt