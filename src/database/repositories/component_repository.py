from sqlalchemy.orm import Session
from database.repositories.base_repository import BaseRepository
from database.models.asset_component import AssetComponentModel

class AssetComponentRepository(BaseRepository[AssetComponentModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ quản lý các thành phần tài nguyên ngoại hình chi tiết"""
		super().__init__(db_session, AssetComponentModel)

	def get_components_by_asset(self, asset_id: int) -> list[AssetComponentModel]:
		"""Truy vấn lấy ra toàn bộ các bộ phận ngoại hình (tóc, mặt, trang phục...) của một thực thể cha"""
		return self.db.query(self.model).filter(self.model.asset_id == asset_id).all()

	def get_specific_component_prompt(self, asset_id: int, component_type: str) -> str:
		"""Truy vấn nhanh chuỗi prompt nghệ thuật của một bộ phận cụ thể (Ví dụ: Lấy prompt tóc của Tô Mộc)"""
		comp = self.db.query(self.model).filter(
			self.model.asset_id == asset_id,
			self.model.type == component_type.lower()
		).first()
		return comp.prompt if comp else ""