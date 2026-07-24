from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class ProjectModel(Base):
	__tablename__ = "projects" # Khớp chính xác phân khu Project Management của DreamForge Engine

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(150), nullable=False, unique=True)    # Tên dự án phim hoạt hình (Ví dụ: Toàn Dân Tạo Mộng)
	description = Column(Text, nullable=True)                  # Mô tả ngắn gọn về lộ trình dự án
	author = Column(String(100), nullable=False, default="Harukj")
	
	status = Column(String(50), default="In Production")        # Trạng thái dự án: In Production, Completed
	version = Column(String(20), default="1.0.0")               # Phiên bản phần mềm đóng gói dự án
	
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<ProjectModel(id={self.id}, name='{self.name}', status='{self.status}')>"
