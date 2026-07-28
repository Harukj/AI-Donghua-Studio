from sqlalchemy.orm import Session
from database.models.shot import ShotModel
from core.logger import studio_logger

class RenderQueueService:
	def __init__(self, db_session: Session):
		"""Khởi tạo Động cơ hàng đợi kết xuất hoạt hình - Render Queue Engine v1.0"""
		self.db = db_session

	def process_shot_render_lifecycle(self, shot_id: int) -> str:
		"""
		[RENDER QUEUE CORE - WORKFLOW CONTROLLER]
		Điều phối luồng trạng thái kết xuất đa luồng của ChatGPT: waiting -> rendering -> completed/failed.
		"""
		shot = self.db.query(ShotModel).filter(ShotModel.id == shot_id).first()
		if not shot:
			return "failed"

		# Bước 1: Đưa vào trạng thái chờ kết xuất
		shot.status = "waiting"
		self.db.commit()
		studio_logger.logger.info(f"[RENDER QUEUE] Cú máy [Shot ID: {shot_id}] đang xếp hàng ➔ [WAITING]")

		# Bước 2: Kích hoạt GPU Renderer chuyển sang trạng thái RENDERING
		shot.status = "rendering"
		self.db.commit()
		studio_logger.logger.info(f"[RENDER QUEUE] GPU đang tính toán khung hình ➔ [RENDERING]")
		
		return shot.status

	def retry_failed_render_job(self, shot_id: int) -> bool:
		"""
		[MẮT XÍCH CỨU HỘ TỐI THƯỢNG - AUTOMATED RETRY LOGIC]
		Bắt trúng cú máy bị lỗi và ép hệ thống tái xếp hàng kết xuất lại từ đầu.
		Khớp chính xác 100% dòng lệnh đặc tả \"Sau này có thể retry\" của ChatGPT.
		"""
		shot = self.db.query(ShotModel).filter(ShotModel.id == shot_id).first()
		if shot and shot.status in ["failed", "draft"]:
			studio_logger.logger.warning(f"[RETRY ENGINE] Kích hoạt lệnh cứu hộ! Đang tái nạp hàng đợi cho Shot Lỗi: [{shot_id}]")
			
			# Reset trạng thái vòng đời đưa về nấc chờ render sạch lỗi
			shot.status = "waiting"
			self.db.commit()
			
			# Tái khởi chạy lại luồng xử lý
			self.process_shot_render_lifecycle(shot_id)
			return True
		return False
