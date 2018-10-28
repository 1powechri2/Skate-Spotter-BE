from sqlalchemy import create_engine, Integer, String, Column, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# db_uri = 'postgres://cbykbzbefhmsav:4a2a6f721e80986df053193b3832e8dc2a25ca137e1182db9539ee148d0c4ecd@ec2-54-243-46-32.compute-1.amazonaws.com:5432/d61bemsrv7ku14'
db_uri = 'postgresql://dada:sphyack1@localhost/skate_spotting'

engine = create_engine(db_uri)

Session = sessionmaker(engine)

Base = declarative_base()

class SkateSpot(Base):
    __tablename__ = 'skate_spot'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    name = Column(String(60), nullable=False)
    street_name = Column(String(100), nullable=True)
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
