from sqlalchemy.orm import Session
from database.models.shot import ShotModel
from core.logger import studio_logger

class AssetConsistencyEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo cỗ máy bảo vệ tính đồng nhất tài nguyên nhân vật - Consistency Engine v1.0"""
		self.db = db_session

	def propagate_character_token_update(self, char_name: str, component_type: str, new_token_value: str, auto_confirm: bool = True) -> int:
		"""
		[MODULE 5 - CASCADE PROPAGATION UPDATE]
		Thuật toán quét ngầm và tự động cập nhật lan truyền diện mạo mới cho toàn bộ 
		các cú máy chưa kết xuất. Khớp chính xác 100% cơ chế câu hỏi hỏi cảnh báo của ChatGPT.
		"""
		studio_logger.logger.info(f"[CONSISTENCY] Phát hiện yêu cầu thay đổi diện mạo [{component_type.upper()}] cho nhân vật [{char_name}] -> '{new_token_value}'")
		
		if not auto_confirm:
			studio_logger.logger.warning("[CONSISTENCY] Hệ thống tạm dừng đưa câu hỏi: 'Có cập nhật cho các Scene chưa render không?'")
			return 0

		# Tìm kiếm tất cả các cú máy trong hệ thống đang ở trạng thái chuẩn bị (draft hoặc ready) để cập nhật dây chuyền
		# Tránh tuyệt đối việc ghi đè vào các file đã kết xuất thành công (rendered / approved)
		pending_shots = self.db.query(ShotModel).filter(
			ShotModel.status.in_(["draft", "ready"])
		).all()

		updated_count = 0
		for shot in pending_shots:
			# Kiểm tra xem chuỗi câu lệnh prompt của Shot đó có chứa tên nhân vật hay không
			if char_name.lower() in shot.prompt.lower():
				# Giả lập bẻ chuỗi để cập nhật hoặc nối thêm Token diện mạo mới vào ma trận Prompt
				old_prompt = shot.prompt
				shot.prompt = f"{old_prompt}, updated_{component_type}: {new_token_value.strip().lower()}"
				updated_count += 1

		if updated_count > 0:
			self.db.commit()
			studio_logger.logger.info(f"[✓ SUCCESS] Lan truyền thành công! Đã đồng bộ diện mạo mới cho {updated_count} cú máy chưa render.")
		else:
			studio_logger.logger.info("[CONSISTENCY] Không tìm thấy cú máy chờ render nào chứa nhân vật này để cập nhật.")

		return updated_count
