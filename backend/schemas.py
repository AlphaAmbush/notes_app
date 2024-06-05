from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    description: str | None = None


class NoteCreate(NoteBase):
    pass

    
class Note(NoteBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool | None = None
    notes: list[Note] = []

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None


def main() -> None:
    pass

if __name__ == "__main__":
    main()