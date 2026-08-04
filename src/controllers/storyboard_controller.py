from sqlalchemy.orm import Session
from src.database.repositories.storyboard_repository import StoryboardRepository
from src.ai.scene_splitter.storyboard import StoryboardEngine
from src.core.logger import studio_logger

class StoryboardController:
	def __init__(self, db_session: Session):
		"""
		[CODING STANDARD v1.0 - ARCHITECTURE CONTROLLER LAYER]
		Thành phần trung gian điều phối dòng dữ liệu. 
		Triệt tiêu hoàn toàn việc GUI gọi trực tiếp truy vấn Database bậy bạ.
		"""
		self.db = db_session
		# Thiết lập chuỗi liên kết hạ tầng tuân thủ sơ đồ 5 tầng của ChatGPT
		self.repository = StoryboardRepository(db_session)
		self.engine = StoryboardEngine(repository=self.repository)

	def handle_gui_request_to_slice_chapter(self, episode_id: int, raw_text: str) -> dict:
		"""
		Hứng nhận yêu cầu từ nút bấm của GUI, thực thi bóc tách logic ngầm 
		và xuất kết quả phản hồi trạng thái sạch về cho màn hình hiển thị.
		"""
		studio_logger.logger.info(f"[CONTROLLER] Tiếp nhận gói chỉ thị sản xuất từ tầng GUI cho Tập phim {episode_id}...")
		
		try:
			# Chuyển giao tác vụ xuống cho tầng Engine xử lý chuyên sâu
			scenes_result = self.engine.slice_novel_into_vivid_scenes(episode_id, raw_text)
			
			return {
				"status": "success",
				"message": f"Đã tự động rã mạch truyện thành {len(scenes_result)} phân cảnh vĩ mô.",
				"data": scenes_result
			}
		except Exception as e:
			studio_logger.logger.error(f"[CONTROLLER ERROR] Thất bại khi điều hướng luồng tác vụ: {e}")
			return {"status": "error", "message": str(e), "data": []}
