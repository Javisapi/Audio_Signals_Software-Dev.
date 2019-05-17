"""Database file."""
import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import json

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'  # docker-compose creates a hostname alias with the service name
port = '5432'  # default postgres port
engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Dataset(Base):
    """Dataset table."""

    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    description = Column(String(512))
    date_created = Column(DateTime())

    audioFiles = relationship('AudioFile', back_populates = 'dataset')


class AudioFile(Base):
    """Dataset table."""

    __tablename__ = 'audio_file'
    id = Column(Integer, primary_key=True)
    audio_path = Column(String(256))
    date_created = Column(DateTime())

    # relationships
    id_dataset = Column(Integer, ForeignKey('dataset.id'))
    dataset = relationship('Dataset', back_populates='audioFiles')


def init_db():
    """Import all modules here that might define models.
    # so that they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    """
    Base.metadata.create_all(bind=engine)
    file_handler = open('data.json', 'r')
    parsed_data = json.loads(file_handler.read())
    
    return parsed_data