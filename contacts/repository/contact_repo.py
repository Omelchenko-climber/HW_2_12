from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from .contact_model import Contact


async def get_contact(
        id: int,
        db: Session
):
    try:
        contact = db.get_one(Contact, id)
    except:
        raise HTTPException(status_code=404, detail=f'Contact not found.')

    return contact


async def get_all_contacts(
        db: Session
):
    contacts = db.query(Contact).all()

    return contacts


async def add_contact(
        contact,
        db: Session
):
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


async def delete_contact(
        contact_id: int,
        db: Session
):
    contact = await get_contact(contact_id, db)

    db. delete(contact)
    db.commit()

    return contact


async def update_contact(
        contact_id: int,
        new_contact,
        db: Session
):

    contact = await get_contact(contact_id, db)

    contact.name = new_contact.name if True else contact.name
    contact.surname = new_contact.surname if True else contact.surname
    contact.email = new_contact.email if True else contact.email
    contact.phone_number = new_contact.phone_number if True else contact.phone_number
    contact.date_of_birth = new_contact.date_of_birth if True else contact.date_of_birth
    contact.additional_data = new_contact.additional_data if True else contact.additional_data

    db.commit()
    db.refresh(contact)

    return contact


async def search_contact(
        db: Session,
        name: str = None,
        surname: str = None,
        email: str = None,
):

    result = db.query(Contact)

    if name:
        result = result.filter(Contact.name == name).all()
    if surname:
        result = result.filter(Contact.surname == surname).all()
    if email:
        result = result.filter(Contact.email == email).all()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Contact not found")


async def get_upcoming_birthdays_from_db(db: Session):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        (func.to_char(Contact.date_of_birth, 'MM-DD') >= func.to_char(today, 'MM-DD')) &
        (func.to_char(Contact.date_of_birth, 'MM-DD') <= func.to_char(next_week, 'MM-DD'))
    ).all()

    if contacts:
        return contacts
    else:
        raise HTTPException(status_code=404, detail="Contacts not found")
