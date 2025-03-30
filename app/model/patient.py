from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.utils.date_utils import format_date 
from app.model import Base


class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    personal_id = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(10))
    gender = Column(String(20))
    birth_date = Column(Date, nullable=False)
    address = relationship("Address", uselist=False, back_populates="patient", cascade="all, delete-orphan")

    def __init__(self, name, personal_id, email, phone, gender, birth_date, address=None):
        self.name = name
        self.personal_id = personal_id
        self.email = email
        self.phone = phone
        self.gender = gender
        self.birth_date = birth_date
        self.address = address

    def to_view_schema(self):
        return {
            'id': self.id,
            'personal_id': self.personal_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'gender': self.gender,
            'birth_date': format_date(self.birth_date),
            'address': self.address.to_view_schema() if self.address else None
        }
