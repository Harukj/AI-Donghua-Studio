import unittest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

# Ép đường dẫn đi qua gói src cô lập
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# GIẢI PHÓNG TOÀN DIỆN REGISTRY: Xóa sạch bộ đệm mappers cũ trước khi đăng ký Metadata mới tinh
clear_mappers()

from database.base import Base
from database.models.episode import EpisodeModel
from database.models.shot import ShotModel
from services.package_generator import EpisodePackageGenerator

class TestEpisodePackageSubsystem(unittest.TestCase):
    def setUp(self):
        """Khởi tạo cơ sở dữ liệu giả lập cô lập tuyệt đối trên khay RAM"""
        self.engine = create_engine("sqlite:///:memory:")
        
        # Tiêm tham số mở rộng để ép SQLAlchemy ghi đè mọi metadata cũ nếu có xung đột
        EpisodeModel.__table__.metadata.clear()
        Base.metadata.create_all(self.engine)
        
        SessionLocal = sessionmaker(bind=self.engine)
        self.db = SessionLocal()
        
        # Nạp dữ liệu mẫu bám sát kịch bản truyện chữ phim Donghua
        self.mock_episode = EpisodeModel(
            id=1, project_id="ToanDanTaoPhong", episode_number=1, 
            title="Mở Đầu", summary="Tô Mộc thức tỉnh"
        )
        self.db.add(self.mock_episode)
        self.db.commit()

        self.generator = EpisodePackageGenerator(self.db)

    def test_automated_six_layers_package_generation(self):
        report = self.generator.generate_six_layers_package(episode_id=1, project_id="ToanDanTaoPhong")
        self.assertEqual(report["status"], "success")

    def tearDown(self):
        self.db.close()
        clear_mappers()
