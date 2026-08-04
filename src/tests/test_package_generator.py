import unittest
import sys
import os
import importlib  # TIÊM THƯ VIỆN NẠP CƯỠNG ÉP HỆ THỐNG
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

# 1. Ép đường dẫn đi qua phân khu src cô lập bám sát PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# 2. GIẢI PHÓNG TOÀN DIỆN REGISTRY: Xóa bộ đệm mappers kẹt cũ dứt điểm
clear_mappers()

# 3. CƯỠNG ÉP PYTHON TÁI LẬP METADATA: Bẻ gãy hoàn toàn cơ chế cache mô-đun bảo thủ
import database.models
importlib.reload(database.models)  # Ép nạp lại để giải phóng dứt điểm KeyError 'ShotModel'

from database.base import Base
from database.models.episode import EpisodeModel
from database.models.shot import ShotModel
from services.package_generator import EpisodePackageGenerator


class TestEpisodePackageSubsystem(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cơ sở dữ liệu Sandbox hoàn toàn cô lập trong khay RAM"""
		self.engine = create_engine("sqlite:///:memory:")
		
		# Cưỡng ép làm sạch Metadata cục bộ và dựng lại cấu trúc 4 bảng sạch từ đầu
		Base.metadata.clear()
		Base.metadata.create_all(self.engine)
		
		SessionLocal = sessionmaker(bind=self.engine)
		self.db = SessionLocal()
		
		# Chèn kịch bản tập phim giả lập bám sát luồng xử lý truyện chữ
		self.mock_episode = EpisodeModel(
			id=1,
			project_id="ToanDanTaoPhong",
			episode_number=1,
			title="Mở Đầu",
			summary="Tô Mộc tỉnh lại giữa ma trận không gian."
		)
		self.db.add(self.mock_episode)
		self.db.commit()

		self.generator = EpisodePackageGenerator(self.db)

	def test_automated_six_layers_package_generation(self):
		"""Kiểm duyệt chức năng bóc tách đóng gói tập phim 6 lớp cấu trúc"""
		report = self.generator.generate_six_layers_package(episode_id=1, project_id="ToanDanTaoPhong")
		self.assertEqual(report["status"], "success")

	def tearDown(self):
		self.db.close()
		self.engine.dispose()
