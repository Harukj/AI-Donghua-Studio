from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.base import Base

class CharacterModel(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    alias = Column(String(100), nullable=True)
    gender = Column(String(20), nullable=True)
    age = Column(String(20), nullable=True)
    height = Column(String(20), nullable=True)
    weight = Column(String(20), nullable=True)
    hair = Column(String(100), nullable=True)
    eyes = Column(String(100), nullable=True)
    face = Column(String(100), nullable=True)
    skin = Column(String(100), nullable=True)
    costume = Column(Text, nullable=True)
    weapon = Column(String(100), nullable=True)
    personality = Column(Text, nullable=True)
    voice = Column(String(100), nullable=True)
    style = Column(String(100), nullable=True)
    positive_prompt = Column(Text, nullable=True)
    negative_prompt = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)               # Đường dẫn file ảnh đại diện nhân vật
    seed = Column(String(50), nullable=True)                 # Mã Seed cố định khuôn mặt AI
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}')>"
