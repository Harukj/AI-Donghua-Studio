from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from database.base import Base

# Khai báo kiểu dữ liệu Generic đại diện cho bất kỳ Model Database nào
T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
	def __init__(self, db_session: Session, model: Type[T]):
		"""Khởi tạo kho lưu trữ nhận vào một Session và kiểu dữ liệu Model cụ thể"""
		self.db = db_session
		self.model = model

	def get_by_id(self, id: int) -> Optional[T]:
		"""Truy vấn lấy ra một bản ghi dựa theo ID khóa chính"""
		return self.db.query(self.model).filter(self.model.id == id).first()

	def get_all(self) -> List[T]:
		"""Lấy ra toàn bộ danh sách bản ghi có trong bảng"""
		return self.db.query(self.model).all()

	def create(self, obj_data: dict) -> T:
		"""Thêm mới hoàn toàn một bản ghi thực thể dữ liệu thương mại"""
		db_obj = self.model(**obj_data)
		self.db.add(db_obj)
		self.db.commit()
		self.db.refresh(db_obj)
		return db_obj

	def delete(self, id: int) -> bool:
		"""Xóa bỏ một bản ghi khỏi bảng SQLite dữ liệu"""
		db_obj = self.get_by_id(id)
		if db_obj:
			self.db.delete(db_obj)
			self.db.commit()
			return True
		return False
