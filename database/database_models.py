from .database import Base
from sqlalchemy import Table, Column, String, Integer, text, Float, ForeignKey
from sqlalchemy.orm import relationship


association_table = Table(
    'fish_location_association', 
    Base.metadata, 
    Column('fish_id', Integer, ForeignKey('fishes.id')),
    Column('location_id', Integer, ForeignKey('location.id'))
)

class Location(Base):
    __tablename__  = "location"
    id = Column(Integer, primary_key= True, index = True)
    name = Column(String, index=True)
    region = Column(String)
    fishes = relationship("Fish",
                           secondary=association_table,
                             back_populates="locations")
    
class  Fish(Base):
    __tablename__ = "fishes"
    id = Column(Integer, primary_key=True, nullable= False)
    name = Column(String, index=True)
    description = Column(String, nullable= True)
    locations = relationship("Location",
                             secondary=association_table,
                             back_populates="fishes")