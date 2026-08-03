from sqlalchemy import Column, Integer, String, Text, Float, DateTime
# NẠP BỔ SUNG: Khai báo hàm relationship từ tầng ORM của SQLAlchemy
from sqlalchemy.orm import relationship 
from datetime import datetime
from src.database.base import Base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey # Nạp bổ sung ForeignKey
class ShotModel(Base):
	__tablename__ = "shots"
	__table_args__ = {'extend_existing': True}

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(Integer, ForeignKey('episodes.id'), nullable=False)
	index = Column(Integer, nullable=False) # Thứ tự cú máy trong phân cảnh
	context_type = Column(String(50), default="establishing") # establishing, walking, reaction...

	# --- MODULE 4: 6-STATES LTX WORKSPACE LIFECYCLE ---
	# Trạng thái: draft, ready, rendering, rendered, approved, exported
	status = Column(String(30), default="draft", nullable=False)

	draft_path = Column(String(255), nullable=True) # Tệp ảnh phác thảo
	video_path = Column(String(255), nullable=True) # Tệp clip hoạt hình hoàn chỉnh
	audio_path = Column(String(255), nullable=True) # Tệp giọng lồng tiếng nhân vật

	prompt = Column(Text, nullable=False) # Chuỗi câu lệnh trộn ma trận

	# ĐƯA VÀO ĐÚNG TẦM VỰC CLASS: Khai báo mối quan hệ liên kết ngược với bảng Tập phim
	episode = relationship('EpisodeModel', back_populates='shots', foreign_keys='ShotModel.scene_id')
