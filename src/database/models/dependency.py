from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.database.base import Base
from sqlalchemy.orm import relationship
class CharacterDependencyModel(Base):
	__tablename__ = "character_dependencies" # Khớp chính xác phân hệ Sprint 9 của ChatGPT

	id = Column(Integer, primary_key=True, autoincrement=True)
	character_id = Column(Integer, nullable=False)              # Liên kết với ID của nhân vật trong Character Bible
	character = relationship('CharacterModel', back_populates='dependencies')
	# Đóng gói bộ 6 thuộc tính phụ thuộc cơ học của Unreal Engine style
	hair = Column(String(100), nullable=True, default="black hair")
	face = Column(String(100), nullable=True, default="handsome face")
	body = Column(String(100), nullable=True, default="athletic body")
	costume = Column(String(150), nullable=True, default="academy uniform")
	weapon = Column(String(150), nullable=True, default="none")
	voice = Column(String(100), nullable=True, default="default voice")
	
	# Trường mã Seed ghim để bảo vệ tính đồng nhất hình ảnh qua các tập phim
	locked_seed = Column(String(50), nullable=False, default="23561")
	
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<CharacterDependency(char_id={self.character_id}, costume='{self.costume}', weapon='{self.weapon}')>"