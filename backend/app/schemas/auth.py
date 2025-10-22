from pydantic import BaseModel,EmailStr

class LoginRequest(BaseModel):
    useremail: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"