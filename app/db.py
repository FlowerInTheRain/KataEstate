from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URI = 'postgresql+psycopg2://kata:kataaubay@localhost:5432/kata?options=-csearch_path%3Dkata_python'
engine = create_engine(DATABASE_URI, echo=True)



class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {'schema': 'kata_python'}
    pass

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
