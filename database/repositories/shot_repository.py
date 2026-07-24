from sqlalchemy.orm import Session
from database.base import BaseRepository
from database.models.shot import ShotModel

class ShotRepository(BaseRepository[ShotModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ quản lý danh sách các cú máy, tiêm kết nối database session"""
		super().__init__(db_session, ShotModel)

	def get_shots_by_scene(self, scene_id: int) -> list[ShotModel]:
		"""Truy vấn lấy ra toàn bộ danh sách các cú máy của một Phân cảnh cụ thể sắp xếp theo thứ tự index"""
		return self.db.query(self.model).filter(
			self.model.scene_id == scene_id
		).order_by(self.model.shot_index.asc()).all()

	def update_shot_render_result(self, shot_id: int, video_path: str) -> bool:
		"""Cập nhật đường dẫn file cứng video clip (.mp4) và chuyển đổi trạng thái sang hoàn thành sau khi render xong"""
		shot = self.get_by_id(shot_id)
		if shot:
			shot.video_output_path = video_path
			shot.status = "completed"
			self.db.commit()
			return True
		return False
