import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker


dialect = 'postgresql'
username = str(os.environ.get('DATABASEUSERNAME'))
password = str(os.environ.get('PASSWORD'))
host = 'localhost'
port = 5432
database = str(os.environ.get('DATABASE'))

DB_URL = URL.create(
    drivername=dialect,
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
