from sqlalchemy.orm import Session
# Sửa đường dẫn import chính xác trỏ thẳng vào lớp BaseRepository định nghĩa trong file database/base.py
from database.base import BaseRepository
from database.models.asset import AssetModel

class AssetRepository(BaseRepository[AssetModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ tài nguyên hệ thống, kế thừa BaseRepository"""
		super().__init__(db_session, AssetModel)

	def get_assets_by_project(self, project_id: str) -> list[AssetModel]:
		"""Truy vấn lấy toàn bộ tài nguyên vật lý đang có của một Dự án cụ thể"""
		return self.db.query(self.model).filter(self.model.project_id == project_id).all()

	def get_assets_by_type(self, project_id: str, asset_type: str) -> list[AssetModel]:
		"""Văn lọc tài nguyên theo phân khu (Ví dụ: Chỉ lấy danh sách file Audio của dự án)"""
		return self.db.query(self.model).filter(
			self.model.project_id == project_id,
			self.model.type == asset_type
		).all()

	def check_file_exists(self, project_id: str, file_path: str) -> bool:
		"""Tra xem đường dẫn file này đã từng được đăng ký trong hệ thống chưa để tránh trùng lặp"""
		count = self.db.query(self.model).filter(
			self.model.project_id == project_id,
			self.model.path == file_path
		).count()
		return count > 0
