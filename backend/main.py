from fastapi import Depends, FastAPI, HTTPException, status, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from datetime import timedelta
from pydantic import TypeAdapter

from . import crud, models, schemas
from .database import engine, get_db
from .security import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_refresh_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/register", response_model=schemas.User)
def create_user(
        username: Annotated[str, Form()], 
        password: Annotated[str, Form()], 
        db: Session = Depends(get_db)
    ):
    db_user = crud.get_user_by_email(db, username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, email=username, password = password)

@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
    ) -> schemas.RefreshToken:
    
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return schemas.RefreshToken(access_token=access_token, refresh_token = refresh_token, token_type="bearer")

@app.post("/refresh", response_model=schemas.RefreshToken)
async def refresh_access_token(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        db: Session = Depends(get_db)
    ):

    user = crud.get_user_by_email(db, email=current_user.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    access_token = create_access_token(
        data={"sub": user.email}
    )
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return schemas.RefreshToken(access_token=access_token, refresh_token = refresh_token, token_type="bearer")

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

@app.post("/notes/create", response_model=schemas.Note, status_code=201)
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

@app.delete("/notes/delete/{note_id}", response_model=schemas.Note)
def delete_note_for_user(
        note_id,
        current_user: Annotated[schemas.User, Depends(get_current_user)], 
        db: Session = Depends(get_db)
    ):
    note_in = crud.get_note_by_id(db, note_id=note_id)
    if note_in is None or note_in.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found or not authorized to delete")
    return crud.delete_user_note(db=db, note_id=note_id)


def main() -> None:
    pass

if __name__ == "__main__":
    main()
