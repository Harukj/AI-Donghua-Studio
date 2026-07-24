from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class AssetComponentModel(Base):
	__tablename__ = "asset_components" # Khớp chính xác tên bảng trong đặc tả hình ảnh của ChatGPT

	id = Column(Integer, primary_key=True, autoincrement=True)
	asset_id = Column(Integer, nullable=False)                 # ID liên kết trỏ về thực thể cha (Ví dụ: ID nhân vật Tô Mộc)
	type = Column(String(50), nullable=False)                  # Lọc loại: 'hair', 'face', 'body', 'costume', 'weapon'
	name = Column(String(100), nullable=False)                 # Tên thành phần phân loại (Ví dụ: Tóc Tô Mộc)
	version = Column(String(20), default="v1.0")               # Số hiệu phiên bản quản lý
	prompt = Column(Text, nullable=False)                      # Từ khóa prompt nghệ thuật đóng băng (Ví dụ: Long Black Hair)
	seed = Column(String(50), nullable=True)                    # Mã hạt giống đóng băng tính nhất quán
	image = Column(String(255), nullable=True)                 # Đường dẫn file ảnh chân dung thành phần đơn lẻ (nếu có)
	
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<AssetComponent(id={self.id}, type='{self.type}', prompt='{self.prompt}')>"