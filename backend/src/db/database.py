import uuid
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.constants import DB_CONNECTION_STRING

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    # Change UUID to String for SQLite compatibility
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

def get_session():
    # Database connection setup
    DATABASE_URI = DB_CONNECTION_STRING
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session