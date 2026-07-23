from sqlalchemy.orm import Session
from database.repositories.base_repository import BaseRepository
from database.models.character import CharacterModel

class CharacterRepository(BaseRepository[CharacterModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ nhân vật, truyền Model CharacterModel vào lớp cha BaseRepository"""
		super().__init__(db_session, CharacterModel)

	def find_by_name(self, name: str) -> CharacterModel:
		"""Truy vấn lấy ra hồ sơ nhân vật dựa theo tên gọi chính xác"""
		return self.db.query(self.model).filter(self.model.name == name).first()

	def search_by_keyword(self, keyword: str) -> list[CharacterModel]:
		"""Truy vấn tìm kiếm nhân vật gần đúng theo từ khóa (Tên hoặc Biệt danh)"""
		return self.db.query(self.model).filter(
			(self.model.name.like(f"%{keyword}%")) | 
			(self.model.alias.like(f"%{keyword}%"))
		).all()

	def get_characters_by_project(self, project_id: str) -> list[CharacterModel]:
		"""Truy vấn danh sách nhân vật được cô lập riêng biệt cho từng Dự án (Project isolation)"""
		# Trường hợp Model của bạn dùng project_id để phân tách dữ liệu
		if hasattr(self.model, 'project_id'):
			return self.db.query(self.model).filter(self.model.project_id == project_id).all()
		return self.get_all()
