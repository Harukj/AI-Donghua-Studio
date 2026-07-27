import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from database.models.shot import ShotModel
from services.production_scheduler import ProductionScheduler
from database.repositories.shot_repository import ShotRepository

class TestProductionSchedulerAndTimeline(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc bảng SQLite và tiêm môi trường kiểm thử"""
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		self.scheduler = ProductionScheduler(self.db)
		self.shot_repo = ShotRepository(self.db)

		# Tạo sẵn một bản ghi Shot mẫu trong DB để phục vụ kiểm thử kéo giãn thời lượng Timeline
		self.test_shot = ShotModel(
			id=150101, scene_id=1501, index=1, camera="Wide Shot", lens="24mm",
			movement="Slow Pan", duration=3.0, lighting="Morning", prompt="3d test shot"
		)
		self.db.add(self.test_shot)
		self.db.commit()

	def test_scheduler_matrix_and_timeline_stretching(self):
		"""Ca kiểm thử tối thượng: Xác thực bộ điều phối sản xuất lập lịch khép kín và tính năng kéo giãn thời lượng Shot"""
		# 1. Tích kiểm luồng chạy của Production Scheduler (Module lớn nhất)
		mock_novel_data = ["Chương 15: Khởi đầu trận chiến vĩ đại"]
		report = self.scheduler.schedule_episode_production_matrix(
			project_id="ToanDanTaoPhong", episode_num=15, raw_novel_chapters=mock_novel_data
		)
		self.assertEqual(report["episode"], "Episode_15")
		self.assertEqual(report["storyboard_node"]["assigned_scenes_count"], 42)

		# 2. Tích kiểm tính năng kéo dài/rút ngắn Shot trên Timeline Engine
		# Giả lập thao tác kéo thanh Timeline tăng thời lượng từ 3.0 giây lên 5.5 giây điện ảnh
		update_success = self.shot_repo.update_shot_duration_linear(shot_id=150101, new_duration=5.5)
		self.assertTrue(update_success)
		
		# Truy vấn lại DB xem dữ liệu đã được lưu cứng ổn định chưa
		updated_shot = self.shot_repo.get_by_id(150101)
		self.assertEqual(updated_shot.duration, 5.5)

	def tearDown(self):
		"""Dọn dẹp bản ghi test và đóng phiên làm việc"""
		self.db.delete(self.test_shot)
		self.db.commit()
		self.db.close()

if __name__ == "__main__":
	unittest.main()
