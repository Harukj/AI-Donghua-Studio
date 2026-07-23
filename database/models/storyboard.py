from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from database.base import Base

class StoryboardSceneModel(Base):
	__tablename__ = "scenes" # Đổi tên bảng thành 'scenes' theo đúng chuẩn hóa của ChatGPT

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(String(50), nullable=False)              # Mã phân cảnh (Ví dụ: SCENE_01)
	chapter_id = Column(Integer, nullable=False)               # Thuộc chương số mấy (Liên kết bảng Chapters)
	title = Column(String(200), nullable=True)                 # Tiêu đề phân cảnh
	summary = Column(Text, nullable=True)                      # Tóm tắt kịch bản phân cảnh
	
	# Các trường Assets lưu trữ dạng chuỗi phân tách bằng dấu phẩy (hoặc JSON Text) để map với Object
	characters = Column(Text, nullable=True)                   # Các nhân vật xuất hiện
	environments = Column(Text, nullable=True)                 # Các bối cảnh không gian
	props = Column(Text, nullable=True)                        # Vũ khí, bảo vật sử dụng
	dialogues = Column(Text, nullable=True)                    # Danh sách lời thoại cấu trúc
	
	duration = Column(Float, default=5.0)                      # Thời lượng shot phim AI (giây)
	generated_prompt = Column(Text, nullable=True)             # Trường chứa LTX Prompt sinh từ Prompt Engine
	project_id = Column(String(100), nullable=False)           # Định danh cô lập theo dự án
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<SceneModel(id={self.scene_id}, project='{self.project_id}')>"
