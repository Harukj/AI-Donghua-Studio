# Bạn bổ sung thêm 2 dòng import này vào phần đầu file database/init_db.py:
from src.database.models.video import VideoModel
from src.database.models.audio import AudioModel
from src.database.models.episode import EpisodeModel

from src.database.base import Base
from src.database.engine import engine

import src.database.models.project

def init_database():

    Base.metadata.create_all(bind=engine)