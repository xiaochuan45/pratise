from sqlalchemy import Column, Integer, String
from app.database import Base

class Ship(Base):
    __tablename__ = "ships"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, index=True)
    mmsi = Column(String(9), nullable=False, unique=True, index=True)
    ship_type = Column(String(30), nullable=False)
    status = Column(String(20), nullable=False, index=True)
    owner = Column(String(100), nullable=True)
