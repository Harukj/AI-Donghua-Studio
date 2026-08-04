from sqlalchemy.orm import Session
from src.database.repositories.base_repository import BaseRepository
from src.database.models.shot import ShotModel

class ShotRepository(BaseRepository[ShotModel]):
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ quản lý danh sách các cú máy, tiêm kết nối database session"""
		super().__init__(db_session, ShotModel)

	def get_shots_by_scene(self, scene_id: int) -> list[ShotModel]:
		"""Truy vấn lấy ra toàn bộ danh sách các cú máy của một Phân cảnh cụ thể sắp xếp theo thứ tự index"""
		return self.db.query(self.model).filter(
			self.model.scene_id == scene_id
		).order_by(self.model.shot_index.asc()).all()

	def update_shot_render_result(self, shot_id: int, video_path: str) -> bool:
		"""Cập nhật đường dẫn file cứng video clip (.mp4) và chuyển đổi trạng thái sang hoàn thành sau khi render xong"""
		shot = self.get_by_id(shot_id)
		if shot:
			shot.video_output_path = video_path
			shot.status = "completed"
			self.db.commit()
			return True
		return False
	def update_shot_duration_linear(self, shot_id: int, new_duration: float) -> bool:
		"""
		[TIMELINE ENGINE DYNAMIC DURATION LOGIC]
		Cập nhật linh hoạt thời lượng (giây) của cú máy khi người dùng kéo giãn trên thanh Timeline.
		Triệt tiêu hoàn toàn việc cố định khung thời gian cứng, tối ưu hóa nhịp điệu điện ảnh.
		"""
		shot = self.get_by_id(shot_id)
		if shot:
			# Ràng buộc thời lượng tối thiểu là 0.5 giây và tối đa là 30 giây để tránh lỗi kết xuất của AI Renderer
			sanitized_duration = max(0.5, min(new_duration, 30.0))
			shot.duration = sanitized_duration
			self.db.commit()
			
			from src.core.logger import studio_logger
			studio_logger.logger.info(f"[TIMELINE ENGINE] Cú máy [Shot ID: {shot_id}] đã được cập nhật thời lượng mới -> {sanitized_duration}s")
			return True
		return False
	def update_shot_workspace_state(self, shot_id: int, target_status: str) -> bool:
		"""
		[LTX WORKSPACE LIFECYCLE CONTROLLER]
		Điều phối luồng trạng thái 6 nấc chuẩn đặc tả của ChatGPT:
		draft -> ready -> rendering -> rendered -> approved -> exported.
		"""
		valid_states = ["draft", "ready", "rendering", "rendered", "approved", "exported"]
		status_lower = target_status.lower().strip()
		
		if status_lower not in valid_states:
			raise ValueError(f"Trạng thái '{target_status}' không hợp lệ trong hệ thống LTX Workspace!")
			
		shot = self.get_by_id(shot_id)
		if shot:
			shot.status = status_lower
			self.db.commit()
			
			from src.core.logger import studio_logger
			studio_logger.logger.info(f"[LTX WORKSPACE] Cú máy [Shot ID: {shot_id}] đã chuyển trạng thái thành công sang -> [{status_lower.upper()}]")
			return True
		return False
