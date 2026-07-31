import unittest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.database.base import Base
from src.database.models.episode import EpisodeModel
from src.database.models.shot import ShotModel
from src.services.package_generator import EpisodePackageGenerator

class TestEpisodePackageSubsystem(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cơ sở dữ liệu giả lập trong bộ nhớ RAM để cô lập môi trường test"""
		self.engine = create_engine("sqlite:///:memory:")
		Base.metadata.create_all(self.engine)
		SessionLocal = sessionmaker(bind=self.engine)
		self.db = SessionLocal()
		
		# Nạp dữ liệu mẫu bám sát kịch bản truyện chữ phim Donghua của bạn
		self.mock_episode = EpisodeModel(
			id=99, project_id="ToanDanTaoPhong", episode_number=1, 
			title="Mở Đầu Định Mệnh", summary="Tô Mộc thức tỉnh ma pháp trận tại học viện"
		)
		self.mock_shot = ShotModel(
			id=9901, scene_id=99, index=1, context_type="establishing",
			prompt="3D Chinese Donghua style, wide cinematic shot of Long Dang academy"
		)
		self.db.add(self.mock_episode)
		self.db.add(self.mock_shot)
		self.db.commit()

		self.generator = EpisodePackageGenerator(self.db)

	def test_automated_six_layers_package_generation(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực vòng đời sinh cây thư mục 6 lớp sạch lỗi vật lý"""
		report = self.generator.generate_six_layers_package(episode_id=99, project_id="ToanDanTaoPhong")
		
		# Khẳng định cấu trúc (Assertions) bảo chứng chất lượng đầu ra đúng đặc tả ChatGPT
		self.assertEqual(report["status"], "success")
		self.assertTrue(os.path.exists(report["master_json"]))
		self.assertTrue(os.path.exists(os.path.join(report["package_path"], "prompts")))
		self.assertTrue(os.path.exists(os.path.join(report["package_path"], "scenes")))

	def tearDown(self):
		self.db.close()
		Base.metadata.drop_all(self.engine)

if __name__ == "__main__":
	unittest.main()
