from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class Token(BaseModel):
    access_token: str
    token_type: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserList(BaseModel):
    users: list[UserPublic]
