from sqlalchemy.orm import Session
from src.database.repositories.base_repository import BaseRepository
from src.database.models.environment import EnvironmentModel

class EnvironmentRepository(BaseRepository[EnvironmentModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ bối cảnh, kế thừa BaseRepository"""
		super().__init__(db_session, EnvironmentModel)

	def find_by_name(self, name: str) -> EnvironmentModel:
		"""Truy vấn lấy cấu hình bối cảnh dựa theo tên địa danh chính xác"""
		return self.db.query(self.model).filter(self.model.name == name).first()
