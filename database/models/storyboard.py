from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from database.base import Base

class StoryboardSceneModel(Base):
	__tablename__ = "scenes" # Định danh bảng 'scenes' chuẩn theo mô hình v1.0

	id = Column(Integer, primary_key=True, autoincrement=True)
	episode_id = Column(Integer, nullable=False)               # Thuộc tập phim số mấy (Ví dụ: Episode 01)
	chapter_id = Column(Integer, nullable=False)               # Thuộc chương truyện số mấy (Ví dụ: Chapter 01)
	scene_index = Column(Integer, nullable=False)              # Số hiệu phân cảnh tăng dần (Ví dụ: 1, 2, 3...)
	
	title = Column(String(200), nullable=True)                 # Tiêu đề của phân cảnh phim
	summary = Column(Text, nullable=False)                     # Nội dung mô tả hành động chữ thô của cảnh
	duration = Column(Float, default=5.0)                      # Thời lượng shot phim AI (mặc định 5.0 giây)
	
	# Các trường Assets lưu vết thông tin cấu trúc đã được trích xuất
	camera = Column(String(100), nullable=True, default="Medium Shot")
	mood = Column(String(100), nullable=True, default="Epic")
	characters = Column(Text, nullable=True)                   # Lưu mảng tên nhân vật phân tách bằng dấu phẩy
	environments = Column(Text, nullable=True)                 # Lưu bối cảnh không gian
	
	prompt = Column(Text, nullable=True)                       # Chuỗi Prompt gộp cuối cùng cấp cho LTX Studio
	status = Column(String(50), nullable=False, default="draft") # Luồng sản xuất: draft, Approved, Rendering, Completed
	project_id = Column(String(100), nullable=False, default="default") # Cô lập dữ liệu theo từng Project

	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<SceneObject(ep={self.episode_id}, ch={self.chapter_id}, index={self.scene_index}, status='{self.status}')>"
