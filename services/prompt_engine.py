from sqlalchemy.orm import Session

class PromptEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo engine kết nối cơ sở dữ liệu SQLite"""
		self.db = db_session

	def generate_from_scene_object(self, scene) -> str:
		"""
		[PROMPT ENGINE v1.0 - STATIC MIXER CORES]
		Nhận vào thực thể Scene Object -> Bóc tách cơ học bộ 7 thành phần điện ảnh 
		khớp 100% theo đúng sơ đồ khối đặc tả của ChatGPT để sinh câu lệnh LTX Studio.
		"""
		# 1. TRÍCH XUẤT BỘ 3 THÀNH PHẦN TÀI NGUYÊN (ASSETS LAYER)
		character = getattr(scene, 'characters', 'Tô Mộc')
		if isinstance(character, list): character = ", ".join(character)
			
		environment = getattr(scene, 'environments', 'Ký túc xá')
		if isinstance(environment, list): environment = ", ".join(environment)
			
		props = getattr(scene, 'props', '')
		if isinstance(props, list): props = ", ".join(props)
		props_prompt = f"holding {props.lower()}" if props and "none" not in props.lower() else ""

		# 2. TRÍCH XUẤT BỘ 4 THÀNH PHẦN THÔNG SỐ ĐIỆN ẢNH (CINEMATIC LAYER)
		camera_shot = getattr(scene, 'camera', 'Wide Shot')
		mood_atmosphere = getattr(scene, 'mood', 'Mysterious')
		lighting_setup = getattr(scene, 'lighting', 'Morning')
		art_style = getattr(scene, 'style', 'Chinese Donghua 3D animation style')

		# 3. TIẾN HÀNH GHÉP PROMPT CƠ HỌC (STATIC CONCATENATION) THEO TEMPLATE CỐ ĐỊNH
		prompt_elements = [
			f"{art_style.strip()}",
			f"{camera_shot.lower()}",
			f"character {character}",
			f"{props_prompt}",
			f"inside {environment.lower()}",
			f"{lighting_setup.lower()} lighting",
			f"{mood_atmosphere.lower()} atmosphere",
			"masterpiece",
			"cinematic composition",
			"ultra detailed texture",
			"16:9 aspect ratio"
		]
		
		# Lọc sạch các khoảng trống thừa và nối lại bằng dấu phẩy
		final_ltx_prompt = ", ".join([element.strip() for element in prompt_elements if element])
		return final_ltx_prompt
