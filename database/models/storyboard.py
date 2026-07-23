from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from database.base import Base

class StoryboardSceneModel(Base):
	__tablename__ = "storyboard_scenes"

	id = Column(Integer, primary_key=True, autoincrement=True)
	scene_number = Column(String(50), nullable=False)          # Số thứ tự phân cảnh (Ví dụ: Scene 01)
	raw_text = Column(Text, nullable=False)                    # Nội dung văn bản văn học thô của cảnh đó
	
	# --- 5 TRƯỜNG TỰ NHẬN DIỆN THEO ĐẶC TẢ CỦA CHATGPT ---
	character_name = Column(String(100), nullable=True)        # Nhân vật được trích xuất
	environment_name = Column(String(100), nullable=True)      # Bối cảnh không gian được trích xuất
	time_frame = Column(String(50), nullable=True)             # Thời gian (Ngày/Đêm)
	mood_atmosphere = Column(String(100), nullable=True)       # Cảm xúc / Bầu không khí cảnh
	action_description = Column(Text, nullable=True)           # Hành động cụ thể của nhân vật
	# -----------------------------------------------------

	generated_prompt = Column(Text, nullable=True)             # Chuỗi LTX Prompt cuối cùng sau khi trộn
	video_path = Column(String(255), nullable=True)            # Đường dẫn tệp video nháp sau khi AI render
	project_id = Column(String(100), nullable=False, default="default") # Định danh theo dự án
	created_at = Column(DateTime, default=datetime.utcnow)

	def __repr__(self):
		return f"<StoryboardScene(project='{self.project_id}', scene='{self.scene_number}', character='{self.character_name}')>"
