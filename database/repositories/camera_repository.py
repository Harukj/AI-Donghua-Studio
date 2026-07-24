from sqlalchemy.orm import Session
from database.base import BaseRepository
from database.models.camera import CameraModel

class CameraRepository(BaseRepository[CameraModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ quản lý danh sách góc máy ảo, kế thừa BaseRepository"""
		super().__init__(db_session, CameraModel)

	def find_by_preset_name(self, name: str) -> CameraModel:
		"""Truy vấn lấy cấu hình thông số máy quay dựa theo tên định danh chính xác"""
		return self.db.query(self.model).filter(self.model.name == name).first()
