from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from geoalchemy2.types import Geometry as GEOMETRY
from shapely.geometry import Point
from app.database_connection import Base, engine


class Crime(Base):
    __tablename__ = 'crimes'

    id = Column(Integer, primary_key=True, index=True)
    Category = Column(String,nullable=False )
    date = Column(Date, nullable=False)
    quart = Column(String, nullable=False)
    geom = GEOMETRY("POINT",4326)

    area_id = Column(Integer, ForeignKey('areas.id'))
    area = relationship("Area", back_populates="crimes")

Index('idx_crime_area_id', Crime.area_id)

class Area(Base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    area_type = Column(String, nullable=False)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326), nullable=False)

    crimes = relationship("Crime", back_populates="area")

Index('idx_area_geometry', Area.geometry, postgresql_using='gist')


Base.metadata.create_all(bind=engine)