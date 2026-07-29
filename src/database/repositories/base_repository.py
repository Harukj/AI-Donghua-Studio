from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from src.database.base import Base

# ĐỊNH NGHĨA BIẾN KIỂU MẪU (VÁ TRIỆT ĐỂ LỖI T IS NOT DEFINED)
# Khởi tạo T đại diện cho bất kỳ thực thể Model nào kế thừa từ lớp Base của SQLAlchemy
T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
	def __init__(self, db_session: Session, model: Type[T]):
		"""Khởi tạo kho lưu trữ nhận vào một Session và kiểu dữ liệu Model cụ thể"""
		self.db = db_session
		self.model = model

	def get_by_id(self, id: int) -> Optional[T]:
		"""Truy vấn lấy ra một bản ghi thực thể theo ID khóa chính"""
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
