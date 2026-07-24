import os
import json
from core.logger import studio_logger

class PromptBuilder:
	def __init__(self):
		"""Khởi tạo bộ trộn câu lệnh 2.0 nạp thư viện cấu hình tĩnh"""
		self.base_dir = os.path.dirname(os.path.abspath(__file__))
		self.camera_dir = os.path.join(self.base_dir, "camera")

	def _load_preset(self, context_type: str) -> dict:
		"""Đọc tệp tin JSON cấu hình thông số máy quay điện ảnh từ thư viện"""
		preset_map = {
			"establishing": "wide",
			"reaction": "closeup",
			"dialogue": "closeup",
			"action": "wide"
		}
		file_name = preset_map.get(context_type.lower(), "wide")
		file_path = os.path.join(self.camera_dir, f"{file_name}.json")
		
		if not os.path.exists(file_path):
			return {"camera": "Medium Shot", "lens": "50mm", "movement": "Static", "composition": "standard", "duration": 3.5}
			
		with open(file_path, "r", encoding="utf-8") as f:
			return json.load(f)

	def build(self, scene, shot) -> str:
		"""
		[PROMPT BUILDER 2.0 - 7 LAYERS STATIC MIXER]
		Hàm lõi nhận đầu vào đồng thời thực thể Scene và Shot sạch từ cơ sở dữ liệu.
		Thực thi trích xuất ma trận 7 tầng thông tin cơ học khớp 100% sơ đồ khối của ChatGPT.
		"""
		# LỚP 1 & 2: CHARACTER & ENVIRONMENT (Trích xuất tài nguyên Assets sạch từ Scene Object)
		character_part = ", ".join(scene.characters) if hasattr(scene, 'characters') and scene.characters else "Tô Mộc"
		environment_part = ", ".join(scene.environments) if hasattr(scene, 'environments') and scene.environments else "Học viện"

		# LỚP 3: CAMERAPRESET (Tự động nạp thông số góc máy quay ảo từ file JSON cấu hình dựa theo Shot context)
		cam_config = self._load_preset(shot.context_type)
		camera_shot = cam_config.get("camera", "Medium Shot")
		lens_spec = cam_config.get("lens", "50mm")
		camera_move = cam_config.get("movement", "Static")
		composition_rule = cam_config.get("composition", "cinematic framing")
		
		# Cập nhật lại thời lượng và góc máy đồng bộ cho đối tượng Shot
		shot.duration = cam_config.get("duration", shot.duration)
		shot.camera = camera_shot

		# LỚP 4 & 5: LIGHTING & MOOD (Lấy bầu không khí sắc thái nghệ thuật từ phân cảnh tổng hợp)
		lighting_part = getattr(scene, 'lighting', 'Morning')
		mood_part = getattr(scene, 'mood', 'Epic')

		# LỚP 6: ACTION (Đoạn mô tả hành động kịch bản thô bẻ nhỏ của riêng Shot quay)
		action_part = shot.prompt.replace("3D Chinese Donghua style, ", "") if hasattr(shot, 'prompt') else ""

		# LỚP 7: SINH PROMPT (Tiến hành lắp ráp Mixer cơ học theo đúng bộ khung Token của Studio)
		prompt_matrix = [
			"3D Chinese Donghua animation style, highly detailed textures",
			f"{camera_shot.lower()}",
			f"shot with {lens_spec} lens",
			f"{camera_move.lower()} camera movement",
			f"{composition_rule.lower()}",
			f"character {character_part}",
			f"inside environment {environment_part.lower()}",
			f"under {lighting_part.lower()} lighting",
			f"{mood_part.lower()} mood atmosphere",
			f"action detail: {action_part.lower()}" if action_part else "",
			"unreal engine 5 render, ray tracing, masterpiece, flawless cinematic composition, 16:9 aspect ratio"
		]

		# Nối chuỗi cơ học chặt chẽ cách nhau bằng dấu phẩy
		final_prompt = ", ".join([tags.strip() for tags in prompt_matrix if tags])
		
		# Đóng băng lưu chuỗi Prompt nghệ thuật hoàn chỉnh vào thuộc tính của thực thể Shot
		shot.prompt = final_prompt
		
		studio_logger.logger.info(f"Prompt Builder 2.0: Đã hoàn tất ma trận sinh Prompt cho [Shot ID: {shot.id}].")
		return final_prompt