from sqlalchemy.orm import Session
from src.services.character_service import CharacterService
from src.services.environment_service import EnvironmentService
from src.ai.prompt_builder.camera_planner import CameraPlanner
from src.ai.prompt_builder.lighting_planner import LightingPlanner
from src.ai.prompt_builder.fx_planner import FXPlanner
from src.ai.prompt_builder.audio_planner import AudioPlanner
from src.core.logger import studio_logger

class PromptBuilder30:
	def __init__(self, db_session: Session):
		self.db = db_session
		self.char_service = CharacterService(db_session)
		self.env_service = EnvironmentService(db_session)
		
		# Khởi tạo trọn vẹn bộ 4 động cơ tham số hóa điện ảnh của ChatGPT
		self.cam_planner = CameraPlanner()
		self.light_planner = LightingPlanner()
		self.fx_planner = FXPlanner()
		self.audio_planner = AudioPlanner()

	def build_matrix_prompt_v3(self, char_name: str, location_name: str, raw_action_text: str, context_type: str) -> dict:
		"""
		[DREAMFORGE ENGINE v0.8 - SUPREME MATRIX MIXER]
		Đọc trực tiếp dữ liệu từ 5 cỗ máy Planner hậu đài độc lập.
		Thực thi nối chuỗi tĩnh cơ học tuyệt đối để xuất câu lệnh LTX Studio ổn định 100%.
		"""
		studio_logger.logger.info("[DREAMFORGE CORE] Tiến hành gộp ma trận tham số điện ảnh tĩnh...")

		# 1. NẠP DỮ LIỆU TÀI NGUYÊN SẠCH TỪ DATABASE SERVICE
		character_tags = self.char_service.get_fixed_character_prompt_tags(char_name)
		environment_tags = self.env_service.get_fixed_environment_prompt_tags(location_name)

		# 2. TRÍCH XUẤT THAM SỐ TỪ BỘ 4 CỐ MÁY PLANNER TĨNH CHUẨN CHATGPT
		cam = self.cam_planner.resolve_shot_camera_directives(context_type)
		light = self.light_planner.resolve_shot_lighting_directives("morning")
		fx = self.fx_planner.resolve_shot_fx_directives(context_type)
		audio = self.audio_planner.resolve_music_and_voice_directives(context_type)

		# 3. LẮP RÁP CHUỖI TĨNH MA TRẬN PHÂN LỚP QUY CHUẨN ĐỒ HỌA THƯƠNG MẠI
		prompt_matrix = [
			"3D Chinese Donghua animation style, highly detailed textures",
			f"{cam['camera'].lower()}",
			f"shot with {cam['lens']} lens",
			f"{cam['movement'].lower()} movement at {cam['height'].lower()}",
			f"character portrait profile: {character_tags}",
			f"inside setting environment: {environment_tags.lower()}",
			f"under professional {light['type'].lower()} {light['name'].lower()} with dynamic {light['fx'].lower()}",
			f"environmental fx overlay: {fx['wind']}, {fx['leaves']}, {fx['dust']}, {fx['fog']}",
			f"action description scene text: {raw_action_text.strip().lower()}",
			"unreal engine 5 render, ray tracing, flawless framing, masterpiece, 16:9 cinematic aspect ratio"
		]

		positive_prompt = ", ".join([tags.strip() for tags in prompt_matrix if tags])
		negative_prompt = "low quality, blurry, 2d style, sketch, anime, text, watermark, bad lighting"

		# Lưu vết cấu hình âm thanh phục vụ luồng sinh audio tự động kế tiếp
		return {
			"positive": positive_prompt,
			"negative": negative_prompt,
			"audio_directives": audio
		}
