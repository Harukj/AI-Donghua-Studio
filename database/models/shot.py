from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from database.base import Base

class ShotModel(Base):
	__tablename__ = "shots" # Khớp chính xác tên bảng trong đặc tả v0.6

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(Integer, nullable=False)                  # Khóa liên kết trỏ về bảng phân cảnh 'scenes'
	index = Column(Integer, nullable=False)                     # Thứ tự cú máy tăng dần (Ví dụ: 1, 2, 3...)
	
	# Bộ thông số cinematic điều khiển góc nhìn ảo giống Blender/Unreal Engine
	camera = Column(String(100), default="Medium Shot")         # Khung hình góc máy quay
	lens = Column(String(50), default="Standard 50mm")          # Tiêu cự loại ống kính sử dụng
	movement = Column(String(100), default="Static")            # Nhịp chuyển động camera (Slow Zoom, Pan...)
	duration = Column(Float, default=3.0)                       # Thời lượng render của riêng shot (giây)
	lighting = Column(String(100), default="Morning")           # Cấu hình bộ lọc ánh sáng nghệ thuật
	seed = Column(String(50), nullable=True)                    # Mã hạt giống đóng băng tính nhất quán nhân vật
	
	prompt = Column(Text, nullable=False)                       # Câu lệnh prompt nghệ thuật gộp cuối cùng
	video_path = Column(String(255), nullable=True)             # Đường dẫn tệp tin video clip thô thành phẩm (.mp4)
	status = Column(String(50), default="waiting")              # Vòng đời: waiting, rendering, completed

	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<ShotModel(id={self.id}, scene={self.scene_id}, idx={self.index}, status='{self.status}')>"
