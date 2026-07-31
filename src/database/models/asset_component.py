from sqlalchemy import Column, Integer, String, Text, Float, DateTime
# NẠP BỔ SUNG: Khai báo hàm relationship từ tầng ORM để giải phóng lỗi dòng 18
from sqlalchemy.orm import relationship 
from datetime import datetime
from src.database.base import Base

class AssetComponentModel(Base):
	__tablename__ = "asset_components"
	__table_args__ = {'extend_existing': True}

	id = Column(Integer, primary_key=True, autoincrement=True)
	asset_id = Column(Integer, nullable=False) # ID liên kết trỏ về thực thể cha (Ví dụ: ID nhân vật Tô Mộc)
	type = Column(String(50), nullable=False) # Lọc loại: 'hair', 'face', 'body', 'costume', 'weapon'
	name = Column(String(100), nullable=False) # Tên thành phần phân loại (Ví dụ: Tóc Tô Mộc)
	version = Column(String(20), default="v1.0") # Số hiệu phiên bản quản lý
	prompt = Column(Text, nullable=False) # Từ khóa prompt nghệ thuật đóng băng (Ví dụ: Long Black Hair)
	seed = Column(String(50), nullable=True) # Mã hạt giống đồng bộ tính nhất quán
	image = Column(String(255), nullable=True) # Đường dẫn file ảnh chân dung thành phần đơn lẻ (nếu có)
	
	created_at = Column(DateTime, default=datetime.utcnow)
	
	# BẢO VỆ CHUỖI: Sử dụng nháy đơn để bẻ gãy hoàn toàn vòng lặp nạp chéo (Circular Import)
	shots = relationship('ShotModel', back_populates='assets')

	def __repr__(self):
		return f"<AssetComponent(id={self.id}, type='{self.type}', prompt='{self.prompt}')>"
