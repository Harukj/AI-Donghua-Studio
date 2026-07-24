from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from datetime import datetime
from database.base import Base

class ShotModel(Base):
	__tablename__ = "shots" # Khớp chính xác phân khu quản lý của Sprint 8

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(Integer, nullable=False)                  # Liên kết khóa ngoại trỏ về ID của bảng 'scenes'
	shot_index = Column(Integer, nullable=False)                # Thứ tự cú máy trong phân cảnh (Ví dụ: Shot 01, Shot 02)
	
	camera_movement = Column(String(100), default="Static")     # Chuyển động máy quay ảo: Slow Zoom, Panning, Tracking
	frame_size = Column(String(50), default="Medium Close-Up") # Khung hình điện ảnh của riêng shot quay
	
	positive_prompt = Column(Text, nullable=False)              # Câu lệnh prompt đã trộn sạch cấp cho LTX Studio
	video_output_path = Column(String(255), nullable=True)     # Đường dẫn vật lý của file video thô sau khi render (.mp4)
	
	duration = Column(Float, default=3.0)                       # Thời lượng của riêng cú máy (mặc định 3.0 giây)
	status = Column(String(50), default="waiting")              # Trạng thái hàng đợi kết xuất: waiting, rendering, completed
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<ShotObject(scene_id={self.scene_id}, shot_idx={self.shot_index}, status='{self.status}')>"
