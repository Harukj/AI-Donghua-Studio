from sqlalchemy.orm import Session
from database.repositories.base_repository import BaseRepository
from database.models.storyboard import StoryboardSceneModel

class StoryboardRepository(BaseRepository[StoryboardSceneModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ phân cảnh, truyền Model vào lớp cha"""
		super().__init__(db_session, StoryboardSceneModel)

	def get_scenes_by_chapter(self, chapter_id: int) -> list[StoryboardSceneModel]:
		"""Truy vấn lấy danh sách phân cảnh sắp xếp theo thứ tự index tăng dần của một Chương"""
		return self.db.query(self.model).filter(
			self.model.chapter_id == chapter_id
		).order_by(self.model.index.asc()).all()

	def update_scene_status(self, scene_id: int, new_status: str) -> bool:
		"""Cập nhật luồng trạng thái sản xuất phim ('draft', 'Approved', 'Rendering', 'Completed')"""
		valid_statuses = ["draft", "Approved", "Rendering", "Completed"]
		if new_status not in valid_statuses:
			raise ValueError(f"Trạng thái '{new_status}' không hợp lệ trong quy trình sản xuất phim!")
			
		scene = self.get_by_id(scene_id)
		if scene:
			scene.status = new_status
			self.db.commit()
			return True
		return False
