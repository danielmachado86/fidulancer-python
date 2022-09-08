from pydantic.dataclasses import dataclass
from pydantic import BaseModel, EmailStr, validator

class Config:
    validate_assignment = True


class User(BaseModel):
    name: str
    username: str
    email: EmailStr
    mobile: str
    password: str

    @validator("email")
    @classmethod
    def email_valid(cls, value):
        
        return value