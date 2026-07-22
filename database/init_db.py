from database.database import Base
from database.database import engine

def init_database():
    Base.metadata.create_all(bind=engine)
