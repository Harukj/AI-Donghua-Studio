from sqlalchemy.orm import sessionmaker
from database.engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Hàm tiện ích để lấy session kết nối dữ liệu"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
