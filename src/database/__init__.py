from src.database.base import Base
from src.database.engine import engine
from src.database.models.asset import AssetModel
from src.database.models.version import AssetVersionModel
from src.database.models.shot import ShotModel
from src.database.models.dependency import CharacterDependencyModel
from src.database.models.asset_component import AssetComponentModel
from src.database.models.camera import CameraModel

# Khai báo ép kiểu để SQLAlchemy nhận diện toàn bộ các bảng trong hệ thống dữ liệu mới
from src.database.models.novel import NovelModel
from src.database.models.chapter import ChapterModel
from src.database.models.character import CharacterModel
from src.database.models.environment import EnvironmentModel

def init_database():
	# Xây dựng toàn bộ cấu trúc bảng quan hệ sạch v1.0 vào file SQLite
	Base.metadata.create_all(bind=engine)
	print("Hệ thống: Đã khởi tạo cấu trúc cơ sở dữ liệu chuẩn hóa v1.0 thành công.")
