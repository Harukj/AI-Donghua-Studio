from database.base import Base
from database.engine import engine

# Khai báo ép kiểu để SQLAlchemy nhận diện toàn bộ các bảng trong hệ thống dữ liệu mới
from database.models.novel import NovelModel
from database.models.chapter import ChapterModel
from database.models.storyboard import StoryboardSceneModel
from database.models.character import CharacterModel
from database.models.environment import EnvironmentModel

def init_database():
	# Xây dựng toàn bộ cấu trúc bảng quan hệ sạch v1.0 vào file SQLite
	Base.metadata.create_all(bind=engine)
	print("Hệ thống: Đã khởi tạo cấu trúc cơ sở dữ liệu chuẩn hóa v1.0 thành công.")
