from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///database/donghua.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)