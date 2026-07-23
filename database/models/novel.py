from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class NovelModel(Base):
	__tablename__ = "novels"

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(200), nullable=False)                # Tên bộ truyện/tiểu thuyết
	author = Column(String(100), nullable=True)                 # Tên tác giả truyện chữ
	description = Column(Text, nullable=True)                  # Tóm tắt nội dung cốt truyện
	file_path = Column(String(255), nullable=True)             # Đường dẫn file gốc (.txt hoặc .docx) trên máy
	project_id = Column(String(100), nullable=False)           # Thuộc dự án nào để cô lập tài nguyên
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<Novel(id={self.id}, title='{self.title}')>"
