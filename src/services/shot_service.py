from sqlalchemy.orm import Session
from src.database.models.shot import ShotModel
from src.core.logger import studio_logger

class ShotService:
	def __init__(self, db_session: Session):
		"""Khởi tạo Dịch vụ Quản lý Cú máy - Shot Manager v2.0 Core Engine"""
		self.db = db_session

	def split_scene_into_cinematic_shots(self, scene_id: int, raw_scene_text: str) -> list[ShotModel]:
		"""
		[SHOT MANAGER 2.0 - AUTOMATED TIMELINE SPLITTER]
		Tự động phân rã Phân cảnh thành chuỗi 3 cú máy điện ảnh chuyên sâu:
		Establishing (5s) -> Walking (4s) -> Dialogue (4s) chuẩn đặc tả ChatGPT.
		"""
		studio_logger.logger.info(f"[SHOT MANAGER] Tiến hành bẻ nhỏ Scene ID [{scene_id}] thành chuỗi cắt cảnh...")

		# Định nghĩa bộ khung cấu trúc 3 cú máy hạt nhân bất biến của ChatGPT
		blueprints = [
			{"index": 1, "context": "establishing", "duration": 5.0, "camera": "Wide Establishing Shot"},
			{"index": 2, "context": "walking", "duration": 4.0, "camera": "Medium Tracking Shot"},
			{"index": 3, "context": "dialogue", "duration": 4.0, "camera": "Close-Up Dialogue Shot"}
		]

		created_shots = []

		for bp in blueprints:
			# Sinh mã ID duy nhất theo công thức ghép tầng: [SceneID][Index]
			shot_db_id = int(f"{scene_id}{bp['index']:02d}")
			
			# [CƠ CHẾ PHÒNG VỆ CHỐNG TRÙNG ID CHẶNG CUỐI]
			# Quét kiểm tra, nếu ID shot đã tồn tại thì nạp thẳng vào danh sách, tuyệt đối không tạo mới
			existing_shot = self.db.query(ShotModel).filter(ShotModel.id == shot_db_id).first()
			if existing_shot:
				created_shots.append(existing_shot)
				continue

			# Khởi tạo thực thể dữ liệu sạch, sử dụng chính xác cú pháp ngoặc vuông [] truy cập khóa Dictionary
			shot_record = ShotModel(
				id=shot_db_id,
				scene_id=scene_id,
				index=bp["index"],
				context_type=bp["context"],
				status="draft",
				duration=bp["duration"],
				seed="23561",
				prompt=f"3D Chinese Donghua animation style, {bp['camera'].lower()}, action context: {raw_scene_text.strip().lower()}"
			)
			
			self.db.add(shot_record)
			created_shots.append(shot_record)
			studio_logger.logger.info(f" -> [✓] Khởi tạo Shot {bp['index']:02d}: {bp['context'].upper()} | Thời lượng: {bp['duration']}s")

		self.db.commit()
		return created_shots
