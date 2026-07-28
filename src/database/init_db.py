# Bạn bổ sung thêm 2 dòng import này vào phần đầu file database/init_db.py:
from database.models.video import VideoModel
from database.models.audio import AudioModel
from database.models.episode import EpisodeModel

from database.base import Base
from database.engine import engine

import database.models.project

def init_database():

    Base.metadata.create_all(bind=engine)