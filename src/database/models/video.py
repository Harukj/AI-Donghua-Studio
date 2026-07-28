from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class VideoModel(Base):
	__tablename__ = "videos" # Khớp chính xác với tên bảng trong sơ đồ Database mới

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(String(50), nullable=False)              # Liên kết với mã phân cảnh (Ví dụ: SCENE_01)
	prompt_used = Column(Text, nullable=False)                 # Câu lệnh prompt thực tế đã dùng để sinh video
	video_path = Column(String(255), nullable=True)            # Đường dẫn vật lý của file video (.mp4) trong dự án
	resolution = Column(String(20), default="1280x720")         # Độ phân giải kết xuất video
	status = Column(String(50), default="Waiting")             # Trạng thái hàng đợi render (Waiting, Rendering, Done)
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<VideoModel(scene='{self.scene_id}', status='{self.status}')>"
