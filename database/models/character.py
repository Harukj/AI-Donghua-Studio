from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class CharacterModel(Base):
    __tablename__ = "characters"

    # Định nghĩa các trường dữ liệu theo đúng danh sách từ ChatGPT
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)               # Tên nhân vật
    gender = Column(String(20), nullable=True)               # Giới tính
    age = Column(String(20), nullable=True)                  # Tuổi tác
    height = Column(String(20), nullable=True)               # Chiều cao
    hair = Column(String(100), nullable=True)                # Kiểu tóc, màu tóc
    eyes = Column(String(100), nullable=True)                # Đặc điểm đôi mắt
    clothes = Column(Text, nullable=True)                    # Trang phục mặc định
    personality = Column(Text, nullable=True)               # Tính cách / Thần thái
    style = Column(String(100), nullable=True)               # Phong cách vẽ hoạt hình (Anime, 3D...)
    negative_prompt = Column(Text, nullable=True)           # Các đặc điểm cần tránh khi tạo ảnh
    notes = Column(Text, nullable=True)                      # Ghi chú thêm về nhân vật
    created_at = Column(DateTime, default=datetime.utcnow)   # Ngày tạo hồ sơ

    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}')>"
