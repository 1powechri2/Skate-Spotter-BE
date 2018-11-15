from sqlalchemy import create_engine, Integer, String, Column, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from os import environ
import os

# database_url = environ.get('DATABASE_URL')
db_url = 'postgresql://dada:sphyack1@localhost/skate_spotting'
# db_url = database_url

engine = create_engine(db_url)

Session = sessionmaker(engine)

Base = declarative_base()

class SkateSpot(Base):
    __tablename__ = 'skate_spot'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    name = Column(String(60), nullable=False)
    latitude = Column(Float(Precision=64), nullable=False)
    longitude = Column(Float(Precision=64), nullable=False)
    skater_id = Column(Integer, ForeignKey('skater.id'))

    photos = relationship('Photo')

    favorites = relationship('Favorites')

    skaters = relationship(
    'Skater',
    secondary='favorites'
    )

class Skater(Base):
    __tablename__ = 'skater'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    password = Column(String(128), nullable=False)
    tag = Column(String(255))

    spots = relationship('SkateSpot')

    favorites = relationship('Favorites')

    favorite_spots = relationship(
    'SkateSpot',
    secondary='favorites'
    )

class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    spot_id = Column(Integer, ForeignKey('skate_spot.id'))

class Favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    skater_id = Column(Integer, ForeignKey('skater.id'))
    spot_id = Column(Integer, ForeignKey('skate_spot.id'))
    rating = Column(Boolean, default=True)
