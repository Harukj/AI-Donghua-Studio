import unittest
import sys
import os
import importlib
from sqlalchemy import create_engine  # NẠP BỔ SUNG ĐỂ GIẢI QUYẾT NAMEERROR
from sqlalchemy.orm import sessionmaker  # NẠP BỔ SUNG ĐỂ GIẢI QUYẾT NAMEERROR

# 1. Ép đường dẫn đi qua phân khu src chính thống bám sát PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# 2. CƯỠNG ÉP PYTHON RE-HYDRATION: Bẻ gãy hoàn toàn cơ cơ chế cache module bảo thủ
import database.models
importlib.reload(database.models)

from database.base import Base
from database.models.episode import EpisodeModel
from database.models.shot import ShotModel
from services.package_generator import EpisodePackageGenerator


class TestEpisodePackageSubsystem(unittest.TestCase):
    def setUp(self):
        """Khởi tạo cơ sở dữ liệu Sandbox hoàn toàn cô lập trong khay RAM"""
        self.engine = create_engine("sqlite:///:memory:")
        
        # Cưỡng ép làm sạch Metadata cục bộ và dựng lại cấu trúc bảng sạch từ đầu
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
