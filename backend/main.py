import uvicorn
from datetime import date

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sqldb import crud, models, schemas
from sqldb.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# models.fill_db(SessionLocal)

@app.get("/")
async def root():
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    return {"message": f"Nous sommes aujourd'hui le : {d1}"}

### LOGIN

@app.get("/login/{username}", response_model=schemas.User)
def show_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    # else:
    return db_user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/notes/", response_model=schemas.Note)
def create_note_for_user(
    user_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)
):
    return crud.create_user_note(db=db, note=note, user_id=user_id)


@app.get("/users/{user_id}/notes/", response_model=List[schemas.Note])
def read_all_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes

@app.get("/users/{user_id}/notes/{id}", response_model=schemas.Note)
def read_note_by_id(id:int, user_id:int, db: Session = Depends(get_db)):
    note = crud.get_note(db, user_id=user_id, id=id)
    return note

@app.get("/users/{user_id}/text/{date}", response_model=schemas.Note)
def read_note_by_date(date:str, user_id:int, db: Session = Depends(get_db)):
    note = crud.get_text(db, user_id=user_id, date=date)
    return note

@app.patch("/users/{user_id}/notes/{id}", response_model=schemas.Note)
def modify_note_by_id(user_id: int, id: int, note:schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = crud.modify_note(db, note=note, user_id=user_id, id=id)
    return note

@app.delete("/users/{user_id}/notes/{id}", response_model=schemas.Note)
def delete_note_by_id(user_id: int, id: int, db: Session = Depends(get_db)):
    note = crud.delete_note(db, user_id=user_id, id=id)
    return {"message": f"Note {id} deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app")