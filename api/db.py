import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

if os.environ.get("DATABASE_URL"):
    DATABASE_URI = os.environ.get("DATABASE_URL")
else:

    DATABASE_URI = "postgresql://kata:kataaubay@localhost:5432/kata"
engine = create_engine(DATABASE_URI, echo=True)



class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {'schema': 'kata_python'}
    pass

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
