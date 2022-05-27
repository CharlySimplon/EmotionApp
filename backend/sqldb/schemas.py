from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class NoteBase(BaseModel):
    date : str
    note_content: str
    note_sentiment: str 

class NoteCreate(NoteBase):
    user_id : int

class NoteUpdate(NoteBase):
    id: Optional[int]
    user_id: Optional[int]
    date: Optional[str]

class Note(NoteBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username : str



class UserCreate(UserBase):
    is_admin : bool
    password: str


class User(UserBase):
    id: int
    is_admin: bool
    hashed_password : str
    notes: List[Note] = []

    class Config:
        orm_mode = True