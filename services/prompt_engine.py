from sqlalchemy.orm import Session

class PromptEngine:
	def __init__(self, db_session: Session):
		self.db = db_session

	def build_final_ltx_prompt(self, scene_obj) -> str:
		"""
		[SPRINT 7 - PROMPT BUILDER TEMPLATE]
		Tự động bóc tách và lắp ráp 5 tầng thông tin điện ảnh cơ học từ đối tượng kịch bản.
		Triệt tiêu sự ngẫu nhiên của AI, xuất chuỗi prompt chuẩn hóa 100% cho LTX Studio.
		"""
		# 1. Trích xuất tầng Character và Environment từ thuộc tính đối tượng
		character = scene_obj.characters if hasattr(scene_obj, 'characters') and scene_obj.characters else "Tô Mộc"
		if isinstance(character, list): character = ", ".join(character)
			
		environment = scene_obj.environments if hasattr(scene_obj, 'environments') and scene_obj.environments else "Học viện Long Dạng"
		if isinstance(environment, list): environment = ", ".join(environment)

		# 2. Trích xuất tầng thông số điện ảnh nâng cao (Camera, Lighting, Mood)
		camera_shot = getattr(scene_obj, 'camera', 'Wide Shot')
		lighting_setup = getattr(scene_obj, 'lighting', 'Morning')
		mood_atmosphere = getattr(scene_obj, 'mood', 'Epic')

		# 3. Lắp ráp chuỗi Prompt theo Template cố định của Sprint 7
		prompt_template = [
			"masterpiece",
			"3D Chinese Donghua animation style",
			f"{camera_shot.lower()}",
			f"character {character}",
			f"at {environment.lower()}",
			f"{lighting_setup.lower()} lighting",
			f"{mood_atmosphere.lower()} atmosphere",
			"cinematic composition",
			"high detailed texture",
			"16:9 aspect ratio"
		]

		# Nối chuỗi bằng dấu phẩy
		return ", ".join([tags.strip() for tags in prompt_template if tags])
