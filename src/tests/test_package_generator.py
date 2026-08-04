import unittest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

# 1. Ép đường dẫn đi qua phân khu src cô lập
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# 2. GIẢI PHÓNG TOÀN DIỆN REGISTRY: Xóa bộ đệm mappers cũ trước khi dựng Metadata mới tinh
clear_mappers()

# 3. ÉP NẠP TƯỜNG MINH TRỌN GÓI: Kích hoạt toàn bộ danh mục __all__ đăng ký vào SQLAlchemy Registry
import database.models
from database.base import Base
from database.models.episode import EpisodeModel
from database.models.shot import ShotModel
from services.package_generator import EpisodePackageGenerator
from database.base import Base
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
