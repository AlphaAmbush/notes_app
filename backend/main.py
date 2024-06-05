from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from pydantic import TypeAdapter

from . import crud, models, schemas
from .database import engine, get_db
from .security import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
    ) -> schemas.Token:
    
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@app.get("/user", response_model=schemas.User)
async def read_user(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
    ):
    return current_user


@app.get("/notes", response_model=list[schemas.Note])
def read_notes(
        current_user: Annotated[schemas.User, Depends(get_current_user)], 
        db: Session = Depends(get_db)
    ):
    db_user = current_user
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    notes = crud.get_notes(db, user_id=current_user.id)
    return notes

@app.post("/notes/create", response_model=schemas.Note)
def create_note_for_user(
        current_user: Annotated[schemas.User, Depends(get_current_user)], 
        note: schemas.NoteCreate, 
        db: Session = Depends(get_db)
    ):
    return crud.create_user_note(db=db, note=note, user_id=current_user.id)

@app.put("/notes/updates/" , response_model=schemas.Note)
def update_note_for_user(
        current_user: Annotated[schemas.User, Depends(get_current_user)], 
        note : schemas.Note,
        db: Session = Depends(get_db)
    ):  
    note_in_db = crud.get_note_by_id(db, note_id=note.id)
    if note_in_db is None or note.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found or not authorized to delete")
    return crud.update_user_note(db=db, note=note)

@app.delete("/notes/delete/{note}", response_model=schemas.Note)
def delete_note_for_user(
        note_id: int,
        current_user: Annotated[schemas.User, Depends(get_current_user)], 
        db: Session = Depends(get_db)
    ):
    note = crud.get_note_by_id(db, note_id=note_id)
    if note is None or note.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found or not authorized to delete")
    return crud.delete_user_note(db=db, note_id=note_id)


def main() -> None:
    pass

if __name__ == "__main__":
    main()
