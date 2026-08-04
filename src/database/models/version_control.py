from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database.base import Base

class AssetVersionModel(Base):
	__tablename__ = "asset_version_control"
	
	__table_args__ = {'extend_existing': True}

	id = Column(Integer, primary_key=True, autoincrement=True)
	character_name = Column(String(100), nullable=False)       # Tên nhân vật ghim cứng (Ví dụ: Tô Mộc)
	episode_number = Column(Integer, nullable=False)           # Số tập phim liên kết (Ví dụ: 1, 2, 15)
	version_tag = Column(String(50), default="Version 1")      # Nhãn nhãn phiên bản: Version 1, Version 2, Version 3
	
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<AssetVersionModel(char='{self.character_name}', ep={self.episode_number}, tag='{self.version_tag}')>"
