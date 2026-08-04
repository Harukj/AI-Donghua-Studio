from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.database.base import Base

class AudioModel(Base):
	__tablename__ = "audios" # Khớp chính xác với tên bảng trong sơ đồ Database mới

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_id = Column(String(50), nullable=False)              # Liên kết với mã phân cảnh
	dialogue_text = Column(Text, nullable=True)                # Nội dung lời thoại chữ cần chuyển thành giọng nói
	voice_actor_model = Column(String(100), nullable=True)      # Tên model giọng đọc AI (Ví dụ: Lâm Uyển Voice, Tô Mộc Voice)
	audio_path = Column(String(255), nullable=True)            # Đường dẫn vật lý của file âm thanh (.mp3)
	audio_type = Column(String(50), default="Voiceover")       # Phân loại âm thanh (Voiceover, BGM, SFX)
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<AudioModel(scene='{self.scene_id}', type='{self.audio_type}')>"
