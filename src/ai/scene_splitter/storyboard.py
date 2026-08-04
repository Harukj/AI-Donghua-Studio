from src.database.repositories.storyboard_repository import StoryboardRepository
from src.core.logger import studio_logger

class StoryboardEngine:
	def __init__(self, repository: StoryboardRepository):
		"""
		[SOLID & DEPENDENCY INJECTION ARCHITECTURE - QA GATE 1 & 2]
		Tiêm trực tiếp thực thể Repository vào lớp xử lý thay vì gọi Session cứng.
		"""
		self.repository = repository
		self.cache_memory = {} # Khởi tạo vùng nhớ đệm Cache tạm thời (QA Gate 5)

	def slice_novel_into_vivid_scenes(self, episode_id: int, raw_novel_text: str) -> list[dict]:
		"""
		[INVERSION OF CONTROL PIPELINE]
		Bóc tách văn bản chương truyện chữ thô và ủy quyền lưu trữ xuống tầng Repository.
		"""
		# Kiểm tra bộ lọc Cache cục bộ để tăng tốc xử lý (QA Gate 5)
		cache_key = f"ep_{episode_id}_hash_{hash(raw_novel_text)}"
		if cache_key in self.cache_memory:
			studio_logger.logger.info("[CACHE HIT] Trả về ma trận phân cảnh nhanh từ vùng nhớ RAM Cache!")
			return self.cache_memory[cache_key]

		studio_logger.logger.info(f"[STORYBOARD] Đang thực thi bóc tách logic đơn nhất (Single Responsibility)...")
		
		if not raw_novel_text.strip():
			return []

		paragraphs = [p.strip() for p in raw_novel_text.split(".") if p.strip()]
		parsed_scenes = []

		for index, paragraph_text in enumerate(paragraphs):
			scene_db_id = int(f"{episode_id}{index + 1:02d}")
			scene_node = {
				"scene_id": scene_db_id,
				"episode_id": episode_id,
				"scene_index": index + 1,
				"scene_text": paragraph_text
			}
			parsed_scenes.append(scene_node)

		# THỰC THI KIẾN TRÚC DI: Gọi tầng Repository lưu trữ cứng xuống DB vật lý
		self.repository.save_bulk_parsed_scenes(parsed_scenes)
		
		# Đóng băng dữ liệu lưu vào RAM Cache
		self.cache_memory[cache_key] = parsed_scenes
		return parsed_scenes
