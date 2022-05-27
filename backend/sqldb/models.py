from sqlalchemy import Integer, ForeignKey, String, Column, Boolean, DateTime
from .database import Base
from sqlalchemy.orm import relationship
import datetime





class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    is_admin = Column(Boolean, default=False)
    username = Column(String)
    hashed_password = Column(String, default="1234")

    notes = relationship("Note", back_populates="users")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(String, default=datetime.date.today().strftime("%d%m%Y"))
    note_content = Column(String(length=500))
    note_sentiment = Column(String)

    users = relationship("User", back_populates="notes")


