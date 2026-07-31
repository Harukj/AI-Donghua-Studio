from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.database.base import Base

class ChapterModel(Base):
	__tablename__ = "chapters"

	id = Column(Integer, primary_key=True, autoincrement=True)
	novel_id = Column(Integer, nullable=False)                 # Liên kết với ID của bộ truyện chữ
	chapter_number = Column(Integer, nullable=False)           # Số thứ tự chương (#1, #2, #3...)
	title = Column(String(200), nullable=False)                # Tiêu đề chương (Khởi đầu, Thiên tài...)
	raw_content = Column(Text, nullable=False)                 # Toàn bộ nội dung chữ thô của chương truyện
	project_id = Column(String(100), nullable=False)           # Thuộc dự án nào để cô lập tài nguyên
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<Chapter(num={self.chapter_number}, title='{self.title}')>"
