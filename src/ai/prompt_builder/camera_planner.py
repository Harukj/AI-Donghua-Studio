from src.core.logger import studio_logger

class CameraPlanner:
	def __init__(self):
		"""Khởi tạo bộ xử lý góc máy ảo thông minh - Camera Planner v0.8"""
		pass

	def resolve_shot_camera_directives(self, context_type: str) -> dict:
		"""
		[CAMERA PLANNER CORE LOGIC]
		Tự động gán ma trận 4 thông số góc máy quay ảo dựa theo loại ngữ cảnh của Shot.
		Khớp chính xác 100% đặc tả hình ảnh Shot 1 của ChatGPT.
		"""
		# Cấu hình mặc định cho Shot 1 (Establishing Shot) đúng theo ảnh mẫu của bạn
		camera_config = {
			"camera": "Wide Shot",
			"lens": "24mm",
			"movement": "Slow Push",
			"height": "Eye Level"
		}
		
		# Tự động rẽ nhánh thông số nếu là cảnh cận hoặc biểu cảm phản ứng (Reaction/Dialogue)
		if context_type.lower() in ["reaction", "dialogue"]:
			camera_config.update({
				"camera": "Close-Up Shot",
				"lens": "85mm",
				"movement": "Static",
				"height": "Eye Level"
			})
			
		studio_logger.logger.info(f"[CAMERA PLANNER] Đã ghim thông số: Khung hình={camera_config['camera']}, Ống kính={camera_config['lens']}, Chuyển động={camera_config['movement']}")
		return camera_config
