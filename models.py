from database import Base
from sqlalchemy import Column, Integer, String

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)

    brand = Column(String)
    model = Column(String)
    price_per_day = Column(Integer)
