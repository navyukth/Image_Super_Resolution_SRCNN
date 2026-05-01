from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.cores.config import settings
from app.db.base import Base
from app.models.job import Job

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    autocomit = False,
    autoflush = False,
    bind = engine
)

Base.metadata.create_all(bind = engine)

