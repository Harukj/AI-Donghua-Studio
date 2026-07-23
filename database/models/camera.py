from sqlalchemy import Column, Integer, String, Text
from database.base import Base

class CameraModel(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)  # Tên góc máy (Ví dụ: Close Up)
    camera_prompt = Column(Text, nullable=False)            # Từ khóa AI tương ứng (Ví dụ: close-up shot, macro detail)

    def __repr__(self):
        return f"<Camera(name='{self.name}')>"
