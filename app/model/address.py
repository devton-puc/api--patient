from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.model import Base


class Address(Base):
    __tablename__ = 'address' 

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    zipcode = Column(String(20), nullable=False)
    address = Column(String(200), nullable=False)
    neighborhood = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    number = Column(String(10), nullable=False)

    patient = relationship("Patient", back_populates="address")

    def __init__(self, zipcode, address, neighborhood, city, state, number):
        self.zipcode = zipcode
        self.address = address
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.number = number

    def to_view_schema(self):
        return {
            'zipcode': self.zipcode,
            'address': self.address,
            'neighborhood': self.neighborhood,
            'city': self.city,
            'state': self.state,
            'number': self.number
        }
