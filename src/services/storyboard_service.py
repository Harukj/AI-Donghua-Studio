from sqlalchemy.orm import Session
from database.models.episode import EpisodeModel
from src.services.prompt_engine import PromptEngine

class StoryboardService:
	def __init__(self, db_session: Session):
		self.db = db_session
		self.prompt_mixer = PromptEngine()

	def parse_literary_script(self, raw_script_text: str, project_id: str = "ToanDanTaoPhong"):
		"""
		[STORYBOARD ENGINE CORE LOGIC]
		Hàm nhận văn bản kịch bản thô và tự động bóc tách, trích xuất thực thể điện ảnh
		"""
		paragraphs = [p.strip() for p in raw_script_text.split("\n\n") if p.strip()]
		scenes_created = []

		for index, text in enumerate(paragraphs, start=1):
			# Sử dụng EpisodeModel chuẩn doanh nghiệp thay thế hoàn toàn cho lớp cũ đã xóa
			db_scene = EpisodeModel(
				project_id=project_id,
				episode_number=index,
				title=f"Phân cảnh số {index}",
				summary=text[:200]
			)
			self.db.add(db_scene)
			scenes_created.append(db_scene)
			
		self.db.commit()
		return scenes_created

	def get_scene_by_id(self, scene_id: int):
		return self.db.query(EpisodeModel).filter(EpisodeModel.id == scene_id).first()

	def update_scene_status(self, scene_id: int, status: str):
		scene = self.get_scene_by_id(scene_id)
		if scene:
			scene.status = status
			self.db.commit()
			return True
		return False
