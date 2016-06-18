from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy_utils import PasswordType

Base = declarative_base()

SCHEMA = 'carlog'

class user(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': SCHEMA}
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(Text, primary_key=True, nullable=False)
    email_confirmed = Column(Boolean, nullable=False, default=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    vehicles = relationship("vehicle", passive_deletes=True)

class vehicle(Base):
    __tablename__ = 'vehicle'
    __table_args__ = {'schema': SCHEMA}
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(user.id, onupdate="CASCADE", ondelete="CASCADE"), nullable = False)
    model = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    plate = Column(Text, nullable=True)
    vin = Column(String(length=20), nullable=True)
    notes = Column(Text, nullable=True)

class fill_up(Base):
    __tablename__ = 'fill_up'
    id = Column(Integer, primary_key=True, nullable=False)
    guid = Column(String(length=32), nullable=True, unique=True)
    vehicle_id = Column(Integer, ForeignKey(vehicle.id, onupdate="CASCADE", ondelete="CASCADE"), nullable = False)