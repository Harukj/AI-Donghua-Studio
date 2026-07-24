from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class CharacterModel(Base):
	__tablename__ = "characters" # Khớp chính xác phân khu Character Bible của DreamForge Engine

	id = Column(Integer, primary_key=True, autoincrement=True)
	project_id = Column(String(100), nullable=False, default="default") # Cô lập tài nguyên theo từng dự án
	name = Column(String(100), nullable=False)                 # Tên nhân vật (Ví dụ: Tô Mộc)
	alias = Column(String(100), nullable=True)                  # Biệt danh kịch bản
	gender = Column(String(20), nullable=True)                  # Giới tính

	# --- 6 TRƯỜNG THÀNH PHẦN THAY THẾ HOÀN TOÀN CHO PROMPT THÔ THEO ĐẶC TẢ CHATGPT ---
	hair = Column(String(100), nullable=True, default="black short hair")
	face = Column(String(100), nullable=True, default="handsome facial features")
	body = Column(String(100), nullable=True, default="slender athletic body")
	eyes = Column(String(100), nullable=True, default="sharp intense eyes")
	costume = Column(String(150), nullable=True, default="standard academy uniform")
	accessories = Column(String(150), nullable=True, default="none") # Phụ kiện hoặc thần binh cầm tay
	# ---------------------------------------------------------------------------------

	image_path = Column(String(255), nullable=True)             # Đường dẫn file ảnh chân dung gốc
	seed = Column(String(50), nullable=False, default="23561") # Mã hạt giống cố định đóng băng khung hình AI
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<Character(id={self.id}, name='{self.name}', seed='{self.seed}')>"