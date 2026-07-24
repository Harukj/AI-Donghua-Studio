from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from database.base import Base

class AssetVersionModel(Base):
	__tablename__ = "asset_versions" # Khớp chính xác phân hệ Version Manager v1.0

	id = Column(Integer, primary_key=True, autoincrement=True)
	asset_id = Column(Integer, nullable=False)                 # Liên kết với ID của tài nguyên trung tâm trong bảng 'assets'
	version_number = Column(String(20), nullable=False)        # Số hiệu phiên bản (Ví dụ: v1.0, v2.0)
	description = Column(String(255), nullable=True)           # Mô tả thay đổi (Ví dụ: Trang phục học viện, Chiến giáp)
	
	# Lưu trữ cấu trúc Prompt và mã Seed đóng băng của riêng phiên bản này [6]
	prompt_tags = Column(Text, nullable=False)
	seed = Column(String(50), nullable=True)
	
	file_path = Column(String(255), nullable=False)            # Đường dẫn tệp tin ảnh/vật lý của riêng phiên bản này
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<AssetVersion(asset_id={self.asset_id}, version='{self.version_number}')>"
