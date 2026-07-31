from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database.base import Base
from sqlalchemy.orm import relationship
class EnvironmentModel(Base):
	__tablename__ = "environments" # Khớp chính xác phân khu dữ liệu v1.0
	__table_args__ = {'extend_existing': True}
	id = Column(Integer, primary_key=True, autoincrement=True)
	project_id = Column(String(100), nullable=False, default="default") # Cô lập dữ liệu theo từng Project
	name = Column(String(150), nullable=False)                 # Tên nhận diện địa danh (Ví dụ: Học viện Long Dạng)
	
	# --- 5 TRƯỜNG THÀNH PHẦN PHÂN RÃ CHUẨN ĐẶC TẢ CỦA CHATGPT ---
	environment = Column(String(150), nullable=False, default="Long Dang Academy")
	architecture = Column(String(100), nullable=True, default="Chinese Fantasy Academy")
	lighting = Column(String(100), nullable=True, default="Morning")
	weather = Column(String(100), nullable=True, default="sunny")
	atmosphere = Column(String(100), nullable=True, default="epic")
	# -----------------------------------------------------------

	image_path = Column(String(255), nullable=True)             # Đường dẫn file ảnh concept tham chiếu
	created_at = Column(DateTime, default=datetime.utcnow)
	shots = relationship('ShotModel', back_populates='environment')

	def __repr__(self):
		return f"<EnvironmentModel(id={self.id}, name='{self.name}', environment='{self.environment}')>"
