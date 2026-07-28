from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from src.database.base import Base

class ShotModel(Base):
	__tablename__ = "shots"
	__table_args__ = {'extend_existing': True}
	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(Integer, nullable=False)
	index = Column(Integer, nullable=False)                    # Thứ tự cú máy trong phân cảnh
	context_type = Column(String(50), default="establishing")   # establishing, walking, reaction, dialogue

	# --- MODULE 4: 6-STATES LTX WORKSPACE LIFECYCLE ---
	# Trạng thái: draft, ready, rendering, rendered, approved, exported
	status = Column(String(30), default="draft", nullable=False) 
	
	draft_path = Column(String(255), nullable=True)            # Tệp ảnh phác thảo
	video_path = Column(String(255), nullable=True)            # Tệp clip hoạt hình hoàn chỉnh
	audio_path = Column(String(255), nullable=True)            # Tệp giọng lồng tiếng nhân vật
	# --------------------------------------------------

	prompt = Column(Text, nullable=False)                      # Chuỗi câu lệnh trộn ma trận
	duration = Column(Float, default=3.0)                      # Thời lượng kết xuất
	seed = Column(String(50), default="23561")                 # Mã hạt giống đồng nhất hình ảnh
	
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<ShotModel(id={self.id}, index={self.index}, status='{self.status}')>"
