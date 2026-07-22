from database.base import Base
from database.engine import engine

import database.models.project

def init_database():

    Base.metadata.create_all(bind=engine)