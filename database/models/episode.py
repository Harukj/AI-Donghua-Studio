from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class EpisodeModel(Base):
	__tablename__ = "episodes" # Khớp chính xác phân lớp 'episodes' trong sơ đồ của ChatGPT

	id = Column(Integer, primary_key=True, autoincrement=True)
	episode_number = Column(Integer, nullable=False)           # Số tập phim (Ví dụ: Tập 1, Tập 2...)
	title = Column(String(200), nullable=True)                 # Tiêu đề riêng của tập phim
	summary = Column(Text, nullable=True)                      # Tóm tắt diễn biến kịch bản tổng quan của tập
	project_id = Column(String(100), nullable=False)           # Liên kết cô lập tài nguyên theo từng Dự án riêng biệt
	status = Column(String(50), default="In Production")       # Trạng thái sản xuất (In Production, Completed)
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<EpisodeModel(num={self.episode_number}, title='{self.title}', project='{self.project_id}')>"
