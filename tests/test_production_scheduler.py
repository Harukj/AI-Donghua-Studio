import unittest
from src.database.session import SessionLocal
from src.database.models.shot import ShotModel
from src.database.repositories.shot_repository import ShotRepository
from src.services.production_scheduler import ProductionScheduler

class TestProductionSchedulerAndTimeline(unittest.TestCase):

	def setUp(self):
		"""Thiết lập phiên kết nối cơ sở dữ liệu SQLite - Cưỡng ép làm sạch cấu trúc bảng lệch"""
		from src.database.base import Base
		from src.database.engine import engine
		
		# 1. Ép hệ thống xóa tất cả các bảng cũ trong tiến trình để giải phóng bộ đệm cache
		Base.metadata.drop_all(bind=engine)
		
		# 2. Tái khởi tạo lại toàn bộ cấu trúc bảng mới chứa đầy đủ cột context_type và lifecycle paths
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.scheduler = ProductionScheduler(self.db)
		self.shot_repo = ShotRepository(self.db)

		# 3. Nạp đối tượng ShotModel mẫu sạch lỗi trường dữ liệu
		self.test_shot = ShotModel(
			id=150101,
			scene_id=1501,
			index=1,
			context_type="establishing",
			draft_path="projects/ToanDanTaoPhong/assets/draft/shot_150101.png",
			video_path="projects/ToanDanTaoPhong/assets/video/shot_150101.mp4",
			audio_path="projects/ToanDanTaoPhong/assets/audio/shot_150101.mp3",
			prompt="3d donghua animation style, wide shot, establishing academy scene",
			duration=3.0,
			seed="23561"
		)
		self.db.add(self.test_shot)
		self.db.commit()
		# Kiểm tra xem Shot mới tạo có trạng thái mặc định là DRAFT không
		fresh_shot = self.shot_repo.get_by_id(150101)
		self.assertEqual(fresh_shot.status, "draft")
		
		# Phát lệnh dịch chuyển trạng thái: Người dùng phê duyệt (Approved) cú máy thành công
		state_moved = self.shot_repo.update_shot_workspace_state(shot_id=150101, target_status="approved")
		self.assertTrue(state_moved)
		
		# Kiểm tra lại DB xem trạng thái đã được khóa cứng ổn định chưa
		self.assertEqual(fresh_shot.status, "approved")
	def test_scheduler_matrix_and_timeline_stretching(self):
		"""Ca kiểm thử tối thượng: Xác thực bộ điều phối sản xuất lập lịch khép kín và tính năng kéo giãn thời lượng Shot"""
		mock_novel_data = ["Chương 15: Khởi đầu trận chiến vĩ đại"]
		report = self.scheduler.schedule_episode_production_matrix(
			project_id="ToanDanTaoPhong", episode_num=15, raw_novel_chapters=mock_novel_data
		)
		self.assertEqual(report["episode"], "Episode_15")

		# 2. Tích kiểm tính năng kéo dài/rút ngắn Shot trên Timeline Engine
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
