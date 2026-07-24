from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class AssetModel(Base):
	__tablename__ = "assets" # Đổi tên bảng thành 'assets' chuẩn theo thiết kế mới

	id = Column(Integer, primary_key=True, autoincrement=True)
	project_id = Column(String(100), nullable=False)           # Định danh thuộc Dự án nào để cô lập tài nguyên
	type = Column(String(50), nullable=False)                  # Phân loại: 'Characters', 'Environment', 'Props', 'Weapons', 'Audio'...
	name = Column(String(200), nullable=False)                 # Tên tệp tài nguyên gốc (Ví dụ: tomoc.png)
	path = Column(String(255), nullable=False)                 # Đường dẫn vật lý đến file cứng trong thư mục dự án
	thumbnail = Column(String(255), nullable=True)             # Đường dẫn file ảnh thu nhỏ (nếu có)
	tags = Column(Text, nullable=True)                        # Từ khóa bổ trợ (Lưu dạng chuỗi phân tách bằng dấu phẩy)
	created_at = Column(DateTime, default=datetime.utcnow)     # Ngày giờ nạp tài nguyên vào hệ thống Engine

	def __repr__(self):
		return f"<AssetModel(id={self.id}, type='{self.type}', name='{self.name}')>"
