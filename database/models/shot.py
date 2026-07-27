from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from database.base import Base

class ShotModel(Base):
	__tablename__ = "shots"

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(Integer, nullable=False)
	index = Column(Integer, nullable=False)                    # Số thứ tự cú máy trong phân cảnh
	context_type = Column(String(50), default="establishing")   # establishing, walking, reaction, dialogue

	# --- MODULE 4: LTX WORKSPACE LIFECYCLE TRACKING FIELDS ---
	draft_path = Column(String(255), nullable=True)            # Đường dẫn tệp ảnh phác thảo phông nền (draft)
	video_path = Column(String(255), nullable=True)            # Đường dẫn tệp clip hoạt hình hoàn chỉnh (video)
	audio_path = Column(String(255), nullable=True)            # Đường dẫn tệp giọng lồng tiếng hội thoại (audio)
	# ---------------------------------------------------------

	prompt = Column(Text, nullable=False)                      # Chuỗi câu lệnh sinh ra từ Prompt Composer
	duration = Column(Float, default=3.0)                      # Thời lượng kết xuất cú máy (giây)
	seed = Column(String(50), default="23561")                 # Mã hạt giống bảo vệ tính đồng nhất hình ảnh
	
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<ShotModel(id={self.id}, index={self.index}, type='{self.context_type}')>"
