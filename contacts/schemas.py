from pydantic import BaseModel, Field, EmailStr, constr

from typing import Optional
from datetime import date


class ContactBase(BaseModel):
    id: Optional[int] = None
    name: str = Field(title='Contact name', min_length=2, max_length=15)
    surname: str = Field(title='Contact surname', min_length=2,max_length=15)
    email: EmailStr = Field(title='Contact email')
    phone_number: str = Field(title='Contact phone number', min_length=10, max_length=15)
    date_of_birth: date = Field(title='Contact date of birth')
    additional_data: Optional[str]

    class Config:
        from_attributes = True


class ContactUpdate(ContactBase):
    id: Optional[int] = None
    name: constr(min_length=2, max_length=15) = None
    surname: constr(min_length=2, max_length=15) = None
    email: EmailStr = None
    phone_number: constr(min_length=10, max_length=15) = None
    date_of_birth: date = None
    additional_data: constr(min_length=0, max_length=250) = None
