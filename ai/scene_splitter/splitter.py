from ai.scene_splitter.scene import SceneObject
from ai.scene_splitter.parser import ScriptParser
from ai.scene_splitter.rules import TRANSITION_KEYWORDS, MAX_WORDS_PER_SCENE
from core.logger import studio_logger

class Splitter:
	def __init__(self, chapter_number: int, chapter_title: str, raw_content: str):
		self.chapter_number = chapter_number
		self.chapter_title = chapter_title
		self.raw_content = raw_content

	def split_into_objects(self) -> list[SceneObject]:
		"""
		[SPRINT 6 - OOP SPLITTER LOGIC]
		Đọc văn bản thô -> Bẻ cảnh -> Đóng gói thẳng thành các thực thể Class SceneObject.
		"""
		studio_logger.logger.info(f"AI Splitter: Đang bẻ cảnh chương {self.chapter_number} theo chuẩn Dataclass...")
		
		# Gọi bộ Parser làm sạch chữ
		lines = ScriptParser.clean_and_normalize(self.raw_content)
		scene_objects = []
		
		for index, line in enumerate(lines, start=1):
			scene_id = f"SCENE_{self.chapter_number:02d}_{index:03d}"
			
			# Tạo lập trực tiếp đối tượng hướng đối tượng từ văn bản dòng truyện chữ
			scene_obj = SceneObject(
				id=scene_id,
				chapter=self.chapter_number,
				title=f"{self.chapter_title} - Cảnh {index:02d}",
				summary=line, # Dòng chữ thô đóng vai trò làm tóm tắt hành động gốc cho AI Director
				duration=5.0  # Mặc định thời lượng shot phim AI 5 giây
			)
			
			# Thuật toán tự động phát hiện cảm xúc và ánh sáng sơ bộ dựa trên quy tắc rules
			if any(kw in line.lower() for kw in ["nhìn lên", "bầu trời"]):
				scene_obj.mood = "Wonder"
				scene_obj.camera = "Over Shoulder, Low Angle"
			
			scene_objects.append(scene_obj)
			
		return scene_objects
