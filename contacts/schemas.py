from pydantic import BaseModel, Field, EmailStr, constr, ConfigDict

from typing import Optional
from datetime import date, datetime


class ContactBase(BaseModel):
    name: str = Field(title='Contact name', min_length=2, max_length=15)
    surname: str = Field(title='Contact surname', min_length=2,max_length=15)
    email: EmailStr = Field(title='Contact email')
    phone_number: str = Field(title='Contact phone number', min_length=10, max_length=15)
    date_of_birth: date = Field(title='Contact date of birth')
    additional_data: Optional[str] = None

    class Config:
        from_attributes = True


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int


class ContactUpdate(ContactBase):
    pass


class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime


class UserResponse(BaseModel):
    user: UserDb
    detail: str = 'User successfully created'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
