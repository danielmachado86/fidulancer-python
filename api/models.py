"""models for user api

"""

import datetime

from bson.objectid import ObjectId as bson_ObjectId
from pydantic import BaseModel, EmailStr, validator
from werkzeug.security import generate_password_hash

from api import get_app_date
from api.app import get_app_objectid


class ObjectId(bson_ObjectId):  # pylint: disable=missing-class-docstring
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, obj):  # pylint: disable=missing-function-docstring
        if not isinstance(obj, bson_ObjectId):
            raise TypeError("ObjectId required")
        return obj


class CreateUserValidator(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """

    id: ObjectId = None
    name: str
    username: str
    email: EmailStr
    mobile: str
    password: str
    created_at: datetime.datetime = None

    class Config:
        validate_asignment = True
        fields = {"id": "_id"}

    @validator("id", pre=True, always=True)
    @classmethod
    def set_id(cls, v):
        return v or get_app_objectid()

    @validator("username")
    @classmethod
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v

    @validator("name")
    @classmethod
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise ValueError("must contain a space")
        return v.title()

    @validator("created_at", pre=True, always=True)
    @classmethod
    def set_created_at_now(cls, v):
        return v or get_app_date()

    @validator("password")
    @classmethod
    def hash_password(cls, password: str) -> str:
        return generate_password_hash(password)

    def get_data(self) -> dict:
        return self.dict(by_alias=True)


class UpdateUserModel(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """

    name: str
    email: EmailStr
    mobile: str


class ChangeUserPasswordModel(BaseModel):
    """Model definition used in the request for user creation

    Args:
        BaseModel: Pydantic parent class
    """

    old: str
    new: str


class UserResponse(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    id: ObjectId
    name: str
    username: str
    email: EmailStr
    mobile: str
    created_at: datetime.datetime

    class Config:
        validate_asignment = True
        fields = {"id": "_id"}

    @validator("id", pre=True, always=True)
    @classmethod
    def set_id(cls, v):
        return v

    def get_data(self) -> dict:
        return self.dict(by_alias=True)


class CredentialsModel(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """

    username: str
    password: str

    class Config:
        validate_asignment = True

    def get_data(self) -> dict:
        return self.dict(by_alias=True)
