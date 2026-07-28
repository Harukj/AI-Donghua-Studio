import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.database.session import SessionLocal
from src.database.base import Base
from src.database.engine import engine
from src.services.shot_service import ShotService

class TestShotManagerV2Subsystem(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc bảng dữ liệu SQLite rỗng trước khi test"""
		from src.database.base import Base
		from src.database.engine import engine
		
		# Cưỡng ép làm dọn sạch metadata cache để áp cấu hình cột mới
		Base.metadata.drop_all(bind=engine)
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.service = ShotService(self.db)

	def test_automated_3_cinematic_shots_generation(self):
		"""Ca kiểm thử nghiệm thu: Xác thực việc bẻ nhỏ Scene 15 ra đúng 3 Shots với mốc thời gian 5s, 4s, 4s"""
		scene_id = 15
		scene_text = "Tô Mộc mở cửa bước vào học viện. Lâm Uyển đang đứng đợi ở sân."

		# Kích hoạt bộ rã cú máy tự động
		output_shots = self.service.split_scene_into_cinematic_shots(scene_id, scene_text)

		print("\n============ KẾT QUẢ NGHIỆM THU SPRINT 10 - SHOT MANAGER 2.0 ============")
		for shot in output_shots:
			print(f"🎬 [Shot ID: {shot.id}] Vị trí: {shot.index} | Ngữ cảnh lõi: {shot.context_type.upper()}")
			print(f"   Thời lượng: {shot.duration} giây | LTX State: {shot.status.upper()}")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng
		self.assertEqual(len(output_shots), 3)
		self.assertEqual(output_shots[0].duration, 5.0)       # Shot 1 bắt buộc phải dài 5 giây (Establishing)
		self.assertEqual(output_shots[1].context_type, "walking") # Shot 2 bắt buộc phải là hành động walking
		self.assertEqual(output_shots[2].duration, 4.0)       # Shot 3 bắt buộc phải dài 4 giây (Dialogue)

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
