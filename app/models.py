from sqlalchemy import Column, String, Integer, TIMESTAMP
from app.database import Base


class User(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default='now()')

