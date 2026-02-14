from sqlalchemy import Column, Integer, String,Date
from sqlalchemy.orm import relationship
from app.database import Base

class Crime(Base):
    __tablename__ = 'crimes'

    id = Column(Integer, primary_key=True, index=True)
    Category = Column(String,nullable=False )
    date = Column(Date, nullable=False)
    quart = Column(String, nullable=False)
    geom = GEOMETRY(Point,4326)

    area_id = Column(Integer, ForeignKey('areas.id'))
    area = relationship("Area", back_populates="crimes")

class Area(Base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    area_type = Column(String, nullable=False)
    geometry = Column(Geometry("POLYGON", srid=4326), nullable=False)

    crimes = relationship("Crime", back_populates="area")