from sqlalchemy.orm import Session
from database.repositories.base_repository import BaseRepository
from database.models.storyboard import StoryboardSceneModel

class StoryboardRepository(BaseRepository[StoryboardSceneModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ quản lý kịch bản phân cảnh phim, kế thừa BaseRepository"""
		super().__init__(db_session, StoryboardSceneModel)

	def get_scenes_by_hierarchy(self, episode_id: int, chapter_id: int) -> list[StoryboardSceneModel]:
		"""
		[SCENE MANAGER CORE QUERY]
		Truy vấn lấy ra danh sách các phân cảnh thuộc chính xác Tập phim và Chương kịch bản yêu cầu.
		Sắp xếp theo thứ tự scene_index tăng dần tăm tắp đúng theo đặc tả sơ đồ của ChatGPT.
		"""
		return self.db.query(self.model).filter(
			self.model.episode_id == episode_id,
			self.model.chapter_id == chapter_id
		).order_by(self.model.scene_index.asc()).all()

	def get_project_scenes_count(self, project_id: str) -> int:
		"""Đếm tổng số lượng phân cảnh hiện có của một Dự án lớn để phục vụ thống kê sản xuất"""
		return self.db.query(self.model).filter(self.model.project_id == project_id).count()
