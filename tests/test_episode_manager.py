import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from database.models.episode import EpisodeModel
from database.models.shot import ShotModel
from services.episode_service import EpisodeService

class TestEpisodeManagerSubsystem(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc bảng SQLite - Cưỡng ép làm sạch ID kẹt từ các session cũ"""
		from database.base import Base
		from database.engine import engine
		
		# 1. Ép hệ thống xóa sạch toàn bộ các bảng cũ trong tiến trình test động
		Base.metadata.drop_all(bind=engine)
		
		# 2. Tái khởi tạo lại bộ bảng mới tinh cho môi trường độc lập
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.service = EpisodeService(self.db)

		# 3. Nạp bản ghi tập phim mẫu
		self.test_ep = EpisodeModel(project_id="ToanDanTaoPhong", episode_number=15, title="Khởi đầu trận chiến vĩ đại")
		
		# Đổi ID bản ghi mẫu cũ từ 150101 thành một ID ngẫu nhiên cao (Ví dụ: 999999) 
		# nhằm tránh tuyệt đối việc va chạm với dải ID tự động sinh (150101, 150102...) của Agent
		self.test_shot = ShotModel(id=999999, scene_id=1501, index=99, status="draft", prompt="test data code")
		
		self.db.add(self.test_ep)
		self.db.add(self.test_shot)
		self.db.commit()


	def test_automated_9_steps_progress_calculation(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực bộ tính tiến độ bóc tách chuẩn mốc 9% checklist của ChatGPT"""
		progress_report = self.service.get_episode_production_progress_hud(
			project_id="ToanDanTaoPhong", episode_num=15
		)
		
		print("\n============ KẾT QUẢ NGHIỆM THU EPISODE MANAGER (MỐC TIẾN ĐỘ 9%) ============")
		print(f" 🎬 Tập phim: \"{progress_report['episode_title']}\"")
		print(f" 📊 Thanh HUD tiến độ tổng lực: {progress_report['progress_percentage']}")
		print(f" ✅ Trạng thái nút chặng cuối [Export Node]: {progress_report['checklist_nodes']['export']}")
		print("============================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertEqual(progress_report["progress_percentage"], "9%")
		self.assertEqual(progress_report["checklist_nodes"]["novel"], "✓ Loaded")

	def tearDown(self):
		self.db.delete(self.test_ep)
		self.db.delete(self.test_shot)
		self.db.commit()
		self.db.close()

if __name__ == "__main__":
	unittest.main()
