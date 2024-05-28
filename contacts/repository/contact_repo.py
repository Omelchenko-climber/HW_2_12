from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException

from contacts.database.models import Contact, User
from contacts.schemas import ContactBase, ContactUpdate, ContactCreate


async def get_contact(
        id: int,
        user: User,
        db: Session
):
    try:
        contact = db.query(Contact).filter(and_(Contact.id == id, Contact.user_id == user.id)).first()
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Contact not found.')

    return contact


async def get_all_contacts(
        user: User,
        db: Session
) -> list[ContactBase]:
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()

    return contacts


async def add_contact(
        body: ContactCreate,
        user: User,
        db: Session
):
    contact = Contact(
        user_id=user.id,
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone_number=body.phone_number,
        date_of_birth=body.date_of_birth,
        additional_data=body.additional_data
        )
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


async def delete_contact(
        contact_id: int,
        user: User,
        db: Session
):
    contact = await get_contact(contact_id, user, db)

    db.delete(contact)
    db.commit()

    return contact


async def update_contact(
        contact_id: int,
        new_contact: ContactUpdate,
        user: User,
        db: Session
):
    contact = await get_contact(contact_id, user, db)

    contact.user_id = contact.user_id
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
        user: User,
        db: Session,
        name: str = None,
        surname: str = None,
        email: str = None,
):
    result = db.query(Contact).filter(Contact.user_id == user.id).all()

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


async def get_upcoming_birthdays_from_db(
        user: User,
        db: Session
):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            (func.to_char(Contact.date_of_birth, 'MM-DD') >= func.to_char(today, 'MM-DD')) &
            (func.to_char(Contact.date_of_birth, 'MM-DD') <= func.to_char(next_week, 'MM-DD'))
        )).all()

    if contacts:
        return contacts
    else:
        raise HTTPException(status_code=404, detail="Contacts not found")
