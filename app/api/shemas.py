from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class UserCreate(User):
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
