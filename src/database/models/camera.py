from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database.base import Base

class CameraModel(Base):
	__tablename__ = "cameras" # Định danh bảng 'cameras' chuẩn kiến trúc v1.0

	id = Column(Integer, primary_key=True, autoincrement=True)
	project_id = Column(String(100), nullable=False, default="default") # Cô lập tài nguyên theo từng dự án
	name = Column(String(100), nullable=False)                 # Tên preset góc máy (Ví dụ: Toàn cảnh, Cận cảnh)
	
	# --- 5 TRƯỜNG THÀNH PHẦN PHÂN RÃ THEO ĐÚNG ĐẶC TẢ CỦA CHATGPT ---
	shot_type = Column(String(100), nullable=False, default="wide shot")
	lens = Column(String(50), nullable=False, default="24mm")
	height = Column(String(100), nullable=False, default="Eye Level")
	movement = Column(String(100), nullable=False, default="Slow Push")
	composition = Column(String(100), nullable=False, default="Rule of Thirds")
	# ----------------------------------------------------------------

	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<CameraModel(id={self.id}, name='{self.name}', shot='{self.shot_type}')>"
