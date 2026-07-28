from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.base import Base

class NovelModel(Base):
	__tablename__ = "novels"

	# Định nghĩa chính xác theo danh mục dữ liệu "Bước 6 - Database"
	id = Column(Integer, primary_key=True, autoincrement=True)
	project_id = Column(String(100), nullable=False, default="default")  # Liên kết ID dự án để cô lập dữ liệu
	title = Column(String(200), nullable=False)                         # Tiêu đề bộ truyện chữ
	filename = Column(String(255), nullable=False)                      # Tên tệp tin gốc (Ví dụ: novel.docx)
	chapter_count = Column(Integer, nullable=False, default=0)          # Tổng số chương bóc tách được
	created_at = Column(DateTime, default=datetime.utcnow)              # Ngày giờ nạp file vào hệ thống

	def __repr__(self):
		return f"<Novel(id={self.id}, title='{self.title}', chapters={self.chapter_count})>"
