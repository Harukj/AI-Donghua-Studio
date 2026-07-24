from sqlalchemy.orm import Session
from services.character_service import CharacterService
from services.environment_service import EnvironmentService
from services.camera_service import CameraService
from core.logger import studio_logger

class PromptBuilder30:
	def __init__(self, db_session: Session):
		"""Khởi tạo cỗ máy ma trận Prompt Builder 3.0, tiêm các dịch vụ phụ thuộc hệ thống"""
		self.db = db_session
		self.char_service = CharacterService(db_session)
		self.env_service = EnvironmentService(db_session)
		self.cam_service = CameraService(db_session)

	def build_matrix_prompt(self, char_name: str, location_name: str, camera_preset: str, raw_action_text: str) -> dict:
		"""
		[PROMPT BUILDER 3.0 - 20 MODULES STATIC MIXER]
		Thuật toán tự động trích xuất cấu trúc và lắp ráp ma trận 20 phân lớp điện ảnh.
		Triệt tiêu hoàn toàn việc nối chuỗi thủ công, ép cấu hình Token đồng nhất 100%.
		"""
		studio_logger.logger.info("[DREAMFORGE CORE] Kích hoạt cỗ máy Prompt Builder 3.0 trộn ma trận...")

		# 1. TRÍCH XUẤT CÁC PHÂN LỚP TÀI NGUYÊN TỪ DATABASE QUA SERVICES LAYERS
		# Tự động gộp bộ 6 thành phần ngoại hình (hair, face, eyes, costume...)
		character_tags = self.char_service.get_fixed_character_prompt_tags(char_name)
		
		# Tự động gộp bộ 5 thành phần không gian (architecture, lighting, weather, atmosphere...)
		environment_tags = self.env_service.get_fixed_environment_prompt_tags(location_name)
		
		# Tự động gộp bộ 5 thành phần thông số máy quay (shot_type, lens, height, movement, composition)
		camera_tags = self.cam_service.get_fixed_camera_prompt_tags(camera_preset)

		# 2. CẤU HÌNH CÁC PHÂN LỚP NGHỆ THUẬT VÀ CHẤT LƯỢNG CỐ ĐỊNH (STYLE & QUALITY MODULES)
		style_part = "3D Chinese Donghua animation style, flawless cinematic 3D render"
		fx_part = "subtle magical energy particles floating in ambient air"
		motion_part = "cinematic fluid movement, high shutter speed clarity"
		quality_part = "unreal engine 5 render, ray tracing, masterpiece, ultra-detailed textures, 8k resolution"
		negative_prompt = "low quality, blurry, 2d style, sketch, anime, bad anatomy, deformed eyes, text, watermark"

		# 3. LẮP RÁP MA TRẬN 20 MODULES THEO ĐÚNG SƠ ĐỒ THỨ TỰ PHÂN CẤP CỦA CHATGPT
		prompt_matrix = [
			style_part,                       # module: style
			character_tags,                   # module: Character (gồm 6 thuộc tính con)
			environment_tags,                 # module: Environment (gồm 5 thuộc tính con)
			camera_tags,                      # module: Camera (gồm 5 thuộc tính con)
			fx_part,                          # module: fx
			motion_part,                      # module: motion
			f"action detail: {raw_action_text.strip().lower()}" if raw_action_text else "", # module: Action
			quality_part                      # module: quality
		]

		# Tiến hành lọc sạch khoảng trống phát sinh và kết chuỗi tĩnh cách nhau bằng dấu phẩy
		positive_prompt = ", ".join([tags.strip() for tags in prompt_matrix if tags])

		studio_logger.logger.info(" -> [MIXER SUCCESS] Ma trận 20 modules đã được đóng gói xuất xưởng thành công.")
		
		# Xuất bản cặp Prompt sạch sẵn sàng cấp thẳng cho cỗ máy Render Queue
		return {
			"positive": positive_prompt,
			"negative": negative_prompt
		}
