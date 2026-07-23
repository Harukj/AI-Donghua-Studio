from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from database.base import Base

class StoryboardSceneModel(Base):
	__tablename__ = "scenes" # Khớp chính xác tên bảng trong đặc tả v1.0

	id = Column(Integer, primary_key=True, autoincrement=True)
	chapter_id = Column(Integer, nullable=False)               # Thuộc chương số mấy
	index = Column(Integer, nullable=False)                    # Số thứ tự phân cảnh (Ví dụ: 1, 2, 3...)
	title = Column(String(200), nullable=True)                 # Tiêu đề ngắn gọn của phân cảnh
	summary = Column(Text, nullable=False)                     # Nội dung kịch bản chữ/hành động thô của cảnh
	duration = Column(Float, default=5.0)                      # Thời lượng shot phim AI (giây)
	camera = Column(String(100), nullable=True)                # Góc máy điện ảnh mặc định (Close up, Wide...)
	mood = Column(String(100), nullable=True)                  # Bầu không khí cảm xúc cảnh (Wonder, Epic...)
	prompt = Column(Text, nullable=True)                       # Câu lệnh prompt nghệ thuật gộp cuối cùng
	
	# Trường quản lý luồng trạng thái sản xuất thương mại chuẩn thiết kế ChatGPT
	# Nhận các giá trị nghiêm ngặt: 'draft', 'Approved', 'Rendering', 'Completed'
	status = Column(String(50), nullable=False, default="draft")
	
	project_id = Column(String(100), nullable=False, default="default") # Cô lập dữ liệu theo Project
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<SceneModel(id={self.id}, index={self.index}, status='{self.status}')>"
