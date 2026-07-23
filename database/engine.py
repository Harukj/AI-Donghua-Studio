import os
from sqlalchemy import create_engine

# Định vị thư mục chứa database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "donghua.db")

# Tạo engine kết nối
engine = create_engine(
    f"sqlite:///{DB_PATH}", 
    echo=True, 
    connect_args={"check_same_thread": False}
)
