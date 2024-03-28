from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from app.config import ENV, config_by_name
from sqlalchemy.engine.create import create_engine

if ENV == 'dev':
    engine = create_engine(
        config_by_name['dev'].SQLALCHEMY_DATABASE_URI
    )
else:
    engine = create_engine(
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
