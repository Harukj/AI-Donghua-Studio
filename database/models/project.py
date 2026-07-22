from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from database.base import Base


class Project(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    novel_name = Column(String)

    author = Column(String)

    description = Column(String)

    version = Column(String, default="0.2.0")

    project_path = Column(String)

    created_at = Column(DateTime, default=datetime.now)

    updated_at = Column(DateTime, default=datetime.now)