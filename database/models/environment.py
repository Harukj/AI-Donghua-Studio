from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class EnvironmentModel(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)               # Tên bối cảnh (Ví dụ: Long Dang City)
    time_of_day = Column(String(50), nullable=True)          # Thời gian (Day, Night, Sunset...)
    weather = Column(String(50), nullable=True)              # Thời tiết (Sunny, Rainy, Foggy...)
    architecture_style = Column(String(100), nullable=True)   # Phong cách (Cyberpunk, Ancient Chinese...)
    description_prompt = Column(Text, nullable=True)         # Prompt mô tả chi tiết không gian
    style = Column(String(100), nullable=True)               # Phong cách hoạt hình đồng bộ
    negative_prompt = Column(Text, nullable=True)           # Đặc điểm cần tránh khi sinh cảnh
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Environment(id={self.id}, name='{self.name}')>"
