import os
import json
from core.logger import studio_logger

class PromptBuilderV2:
	def __init__(self):
		"""Khởi tạo bộ trộn câu lệnh thế hệ 2.0 (Prompt Builder 2.0)"""
		self.base_dir = os.path.dirname(os.path.abspath(__file__))
		self.camera_dir = os.path.join(self.base_dir, "camera")

	def _load_camera_preset(self, context_type: str) -> dict:
		"""Đọc trực tiếp tệp tin JSON thông số góc máy quay ảo dựa theo loại ngữ cảnh"""
		preset_map = {
			"establishing": "wide",
			"reaction": "closeup",
			"dialogue": "closeup",
			"action": "wide"
		}
		
		preset_name = preset_map.get(context_type.lower(), "wide")
		file_path = os.path.join(self.camera_dir, f"{preset_name}.json")
		
		# Luồng cấu hình dự phòng an toàn nếu file bị xóa
		if not os.path.exists(file_path):
			return {"camera": "Medium Shot", "lens": "50mm", "movement": "Static", "composition": "standard", "duration": 3.5}
			
		with open(file_path, "r", encoding="utf-8") as f:
			return json.load(f)

	def build_final_prompt_from_shot(self, shot_obj, art_style: str = "3D Chinese Donghua animation style") -> str:
		"""
		[PROMPT BUILDER 2.0 ENGINE LOGIC]
		Đọc trực tiếp thông số từ file JSON Camera Presets kết hợp thuộc tính Shot Object.
		Không dùng nối chuỗi bằng tay rườm rà, ép luồng token điện ảnh cố định.
		"""
		# 1. Tự động nạp thông số góc máy ảo từ thư viện camera JSON tập trung
		cam_config = self._load_camera_preset(shot_obj.context_type)
		
		camera_shot = cam_config.get("camera", "Medium Shot")
		lens_spec = cam_config.get("lens", "50mm")
		camera_move = cam_config.get("movement", "Static")
		composition_rule = cam_config.get("composition", "cinematic framing")
		
		# Update lại thời lượng đóng gói tối ưu của Shot từ cấu hình camera presets
		shot_obj.duration = cam_config.get("duration", shot_obj.duration)

		# 2. TIẾN HÀNH TRỘN MẢNG THEO ĐÚNG TIÊU CHUẨN ĐÓNG GÓI THƯƠNG MẠI
		prompt_template = [
			f"{art_style}",
			f"{camera_shot.lower()}",
			f"shot with {lens_spec} lens",
			f"{camera_move.lower()} camera movement",
			f"{composition_rule.lower()}",
			f"scene description: {shot_obj.prompt.replace('3D Chinese Donghua style, ', '')}",
			"unreal engine 5 render, ray tracing, flawless texture, masterpiece, 16:9 cinematic aspect ratio"
		]
		
		final_prompt = ", ".join([tags.strip() for tags in prompt_template if tags])
		
		# Ghi đè cập nhật lại chuỗi Prompt sạch hoàn chỉnh vào thực thể Shot Object
		shot_obj.prompt = final_prompt
		
		studio_logger.logger.info(f"Prompt Builder 2.0: Đã cấu trúc hóa Prompt cho [{shot_obj.id}] thành công.")
		return final_prompt
