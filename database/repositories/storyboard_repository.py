from sqlalchemy.orm import Session
from database.models.shot import ShotModel # Nạp thực thể quản lý phân cảnh/cú máy
from core.logger import studio_logger

class StoryboardRepository:
	def __init__(self, db_session: Session):
		"""Khởi tạo kho lưu trữ dữ liệu Storyboard - Repository Pattern (QA Gate 4)"""
		self.db = db_session

	def save_bulk_parsed_scenes(self, scenes_list: list[dict]) -> bool:
		"""Ghi nhận hàng loạt cấu trúc phân cảnh sạch xuống SQLite an toàn trong một phiên giao dịch"""
		try:
			for sc in scenes_list:
				# Kiểm tra xem ID phân cảnh đã tồn tại chưa để tránh lỗi IntegrityError trùng khóa
				# Đóng vai trò làm lớp Cache kiểm tra tại chỗ (QA Gate 5)
				existing = self.db.query(ShotModel).filter(ShotModel.id == sc["scene_id"]).first()
				if existing:
					continue
					
				# Khởi tạo thực thể ghi nhận
				shot_record = ShotModel(
					id=sc["scene_id"],
					scene_id=sc["episode_id"],
					index=sc["scene_index"],
					context_type="establishing",
					status="draft",
					prompt=f"3D Donghua animation, scenario scene block: {sc['scene_text']}",
					duration=3.0,
					seed="23561"
				)
				self.db.add(shot_record)
				
			self.db.commit()
			return True
		except Exception as e:
			self.db.rollback()
			studio_logger.logger.error(f"[REPO ERROR] Lỗi đồng bộ dữ liệu Storyboard xuống SQLite: {e}")
			return False
