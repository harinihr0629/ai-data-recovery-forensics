from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DB_URL, connect_args={"check_same_thread": False} if settings.DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    from database.models import Base as ModelsBase

    ModelsBase.metadata.create_all(bind=engine)
