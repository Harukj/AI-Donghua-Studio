from sqlalchemy.orm import Session
from database.models.storyboard import StoryboardSceneModel
from services.prompt_engine import PromptEngine

class StoryboardService:
	def __init__(self, db_session: Session):
		self.db = db_session
		self.prompt_mixer = PromptEngine(db_session)

	def parse_literary_script(self, raw_script_text: str, project_id: str = "ToanDanTaoPhong"):
		"""
		[STORYBOARD ENGINE CORE LOGIC]
		Hàm nhận văn bản kịch bản thô và tự động bóc tách, trích xuất thực thể điện ảnh
		"""
		# Giả lập bóc tách kịch bản văn học dựa trên các đoạn văn bản (Paragraphs)
		paragraphs = [p.strip() for p in raw_script_text.split("\n\n") if p.strip()]
		
		scenes_created = []
		for index, text in enumerate(paragraphs, start=1):
			scene_num = f"Scene {index:02d}"
			
			# Thuật toán giả lập "AI Director" tự động nhận diện thực thể trong văn bản
			# Sau này phân đoạn này sẽ kết nối với API LLM (như GPT/Gemini) để tự động trích xuất thông minh
			extracted_character = "Tô Mộc" if "Tô Mộc" in text else "Lâm Thanh"
			extracted_env = "Long Dang City" if "thành phố" in text or "mái nhà" in text else "Academy"
			extracted_time = "Night" if "đêm" in text or "tối" in text else "Day"
			extracted_mood = "Epic" if "hùng vĩ" in text or "vô tận" in text else "Calm"
			
			# Khởi tạo bản ghi phân cảnh chi tiết vào Cơ sở dữ liệu SQLite
			db_scene = StoryboardSceneModel(
				scene_number=scene_num,
				raw_text=text,
				character_name=extracted_character,
				environment_name=extracted_env,
				time_frame=extracted_time,
				mood_atmosphere=extracted_mood,
				action_description=text[:150], # Lấy đoạn ngắn làm mô tả hành động thô
				project_id=project_id
			)
			
			# Gọi bộ trộn Prompt Engine đã viết ở Package 3 để tự ghép nối mã Seed và thuộc tính
			mixed_result = self.prompt_mixer.generate_scene_prompt(
				character_name=extracted_character,
				env_name=extracted_env,
				camera_name="Medium Shot", # Mặc định góc quay trung cảnh nếu kịch bản chữ không nói rõ
				lighting="Golden Hour" if extracted_time == "Day" else "Neon",
				mood=extracted_mood
			)
			
			db_scene.generated_prompt = mixed_result.get("prompt")
			
			self.db.add(db_scene)
			scenes_created.append(db_scene)
			
		self.db.commit()
		print(f"Storyboard Engine: Đã tự động bóc tách thành công {len(scenes_created)} phân cảnh nghệ thuật.")
		return scenes_created

	def get_project_storyboard(self, project_id: str) -> list[StoryboardSceneModel]:
		"""Tải toàn bộ danh sách phân cảnh của dự án hiện tại lên bảng hiển thị giao diện"""
		return self.db.query(StoryboardSceneModel).filter(StoryboardSceneModel.project_id == project_id).all()
