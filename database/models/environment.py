from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class EnvironmentModel(Base):
	__tablename__ = "environments"

	# Định nghĩa chính xác theo đặc tả "Database Tạo bảng" của Sprint 4
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False)                 # Tên bối cảnh (Ví dụ: Long Dạng Thành)
	category = Column(String(100), nullable=True)              # Danh mục không gian
	description = Column(Text, nullable=True)                  # Mô tả không gian thô
	prompt = Column(Text, nullable=True)                       # Prompt gốc mô tả bối cảnh cho AI
	negative_prompt = Column(Text, nullable=True)              # Các yếu tố cần tránh khi tạo cảnh
	lighting = Column(String(100), nullable=True)              # Loại ánh sáng mặc định
	weather = Column(String(100), nullable=True)               # Thời tiết (Sunny, Foggy...)
	time_of_day = Column(String(100), nullable=True)            # Thời gian trong ngày (Day, Night...)
	camera_default = Column(String(100), nullable=True)         # Cấu hình góc máy mặc định cho cảnh
	seed = Column(String(50), nullable=True)                   # Mã số Seed cố định không gian
	thumbnail = Column(String(255), nullable=True)             # Đường dẫn tệp tin ảnh thu nhỏ bối cảnh
	notes = Column(Text, nullable=True)                        # Ghi chú nội bộ
	created_at = Column(DateTime, default=datetime.utcnow)     # Ngày giờ khởi tạo bản ghi

	def __repr__(self):
		return f"<Environment(id={self.id}, name='{self.name}', category='{self.category}')>"
