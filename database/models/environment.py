from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class EnvironmentModel(Base):
	__tablename__ = "environments"

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False)                 # Tên bối cảnh
	alias = Column(String(100), nullable=True)                  # Tên gọi khác
	time_of_day = Column(String(50), nullable=True)            # Thời gian (Day, Sunset...)
	weather = Column(String(50), nullable=True)                # Thời tiết (Rainy, Sunny...)
	architecture = Column(String(100), nullable=True)          # Phong cách kiến trúc
	description = Column(Text, nullable=True)                  # Mô tả không gian thô
	style = Column(String(100), nullable=True)                 # Art style (3D Donghua...)
	positive_prompt = Column(Text, nullable=True)             # Từ khóa bổ trợ bối cảnh
	negative_prompt = Column(Text, nullable=True)             # Từ khóa loại trừ
	image = Column(String(255), nullable=True)                 # Đường dẫn ảnh concept cảnh
	project_id = Column(String(100), nullable=False, default="default") # Cô lập theo dự án

	def __repr__(self):
		return f"<Environment(id={self.id}, name='{self.name}')>"
