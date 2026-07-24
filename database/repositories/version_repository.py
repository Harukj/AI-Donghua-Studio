from sqlalchemy.orm import Session
# Sửa chính xác đường dẫn import trỏ vào file database/base.py trong dự án của bạn
from database.repositories.base_repository import BaseRepository
from database.models.version import AssetVersionModel

class AssetVersionRepository(BaseRepository[AssetVersionModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ quản lý phiên bản tài nguyên, kế thừa BaseRepository"""
		super().__init__(db_session, AssetVersionModel)

	def get_versions_by_asset(self, asset_id: int) -> list[AssetVersionModel]:
		"""Truy vấn lấy ra toàn bộ lịch sử tiến hóa (v1, v2, v3...) của một Asset cụ thể"""
		return self.db.query(self.model).filter(
			self.model.asset_id == asset_id
		).order_by(self.model.created_at.desc()).all()

	def get_specific_version(self, asset_id: int, version_num: str) -> AssetVersionModel:
		"""Truy vấn lấy chính xác cấu trúc Prompt/Seed đã đóng băng của một phiên bản cụ thể để ghim render"""
		return self.db.query(self.model).filter(
			self.model.asset_id == asset_id,
			self.model.version_number == version_num
		).first()
