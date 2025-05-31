from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/intelliextractai' # os.getenv("RDS_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
print('SQLALCHEMY_DATABASE_URL', SQLALCHEMY_DATABASE_URL)
print('SQLALCHEMY_DATABASE_URL 11111', os.environ.get('RDS_URL', ''))
print('SQLALCHEMY_ECHO 11111', os.environ.get('SQLALCHEMY_ECHO', 'False'))

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True if os.environ.get('SQLALCHEMY_ECHO', 'False') == 'False' else False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
