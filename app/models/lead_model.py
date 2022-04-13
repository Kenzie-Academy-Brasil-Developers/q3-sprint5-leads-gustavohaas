from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
from dataclasses import dataclass

@dataclass
class Lead(db.Model):
    id: int
    name: str
    email: str
    phone: str
    creation_date: DateTime
    last_visit: DateTime
    visits: int

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    creation_date = Column(DateTime, nullable=False, unique=True)
    last_visit = Column(DateTime, nullable=False)
    visits = Column(Integer, nullable=True)
