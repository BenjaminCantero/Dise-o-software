from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    role: str

class UserEdit(BaseModel):
    role: str

class UserOut(BaseModel):
    username: str
    role: str