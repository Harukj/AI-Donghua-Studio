from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.base import Base

class EpisodeModel(Base):
	__tablename__ = "episodes"
	
	# ÉP SỰ KIỆN GHI ĐÈ: Cho phép mở rộng/nạp lại cấu trúc bảng đã tồn tại trong Metadata mà không gây crash hệ thống
	__table_args__ = {'extend_existing': True}

	id = Column(Integer, primary_key=True, autoincrement=True)
	project_id = Column(String(100), nullable=False) # Thuộc dự án nào (Ví dụ: Toàn Dân Tạo Mộng)
	episode_number = Column(Integer, nullable=False) # Số tập phim (Ví dụ: Tập 15)
	title = Column(String(200), nullable=True) # Tiêu đề riêng của tập phim
	summary = Column(Text, nullable=True) # Tóm tắt cốt truyện cốt lõi

	status = Column(String(50), default="In Progress") # In Progress, Completed
	created_at = Column(DateTime, default=datetime.utcnow)
	
	# BẢO VỆ CHUỖI: Sử dụng nháy đơn để bẻ gãy hoàn toàn vòng lặp nạp chéo (Circular Import)
	shots = relationship('ShotModel', backref='episode', cascade='all, delete-orphan')

	def __repr__(self):
		return f"<EpisodeModel(id={self.id}, episode_number={self.episode_number}, status='{self.status}')>"
