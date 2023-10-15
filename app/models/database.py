import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlalchemy.orm import Session

from app.config import ENV, config_by_name

if ENV == 'dev':
    engine = sqlalchemy.create_engine(
        config_by_name['dev'].SQLALCHEMY_DATABASE_URI
    )
else:
    engine = sqlalchemy.create_engine(
        config_by_name['test'].SQLALCHEMY_DATABASE_URI
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    """
    Function to get the database session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
