from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..schemas import ContactBase, ContactUpdate
from ..dependencies import get_db
from ..repository.contact_model import Contact
from ..repository import contact_repo


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/upcoming_birthdays')
async def get_upcoming_birthdays(
        db: Session = Depends(get_db)
):
    contacts = await contact_repo.get_upcoming_birthdays_from_db(db)

    return contacts


@router.get('/search')
async def search_contact(
        name: Annotated[str | None, Query(alias='name')] = None,
        surname: Annotated[str | None, Query(alias='surname')] = None,
        email: Annotated[str | None, Query(alias='email')] = None,
        db: Session = Depends(get_db)
):
    contact = await contact_repo. search_contact(db, name, surname, email)

    return contact


@router.get('/get_one/{contact_id}', response_model=ContactBase)
async def get_contact(
        contact_id: Annotated[int, Path(title='The id of the contact to get')],
        db: Session = Depends(get_db)
):
    contact = await contact_repo.get_contact(contact_id, db)

    return contact


@router.get('/all', response_model=list[ContactBase])
async def all_contacts(
        db: Session = Depends(get_db)
) -> list[ContactBase]:
    contacts = await contact_repo.get_all_contacts(db)

    return contacts


@router.post('/add')
async def add_new_contact(
        contact: ContactBase,
        db: Session = Depends(get_db),
):
    contact = Contact(**contact.model_dump())

    try:
        contact = await contact_repo.add_contact(contact, db)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=repr(e))

    return contact


@router.delete('/delete/{contact_id}')
async def delete_contact(
        contact_id: Annotated[int, Path(title='The id of the contact to delete.')],
        db: Session = Depends(get_db)
):
    await contact_repo.delete_contact(contact_id, db)

    return {'status': f'contact with id {contact_id} was deleted.'}


@router.put('/update/{contact_id}')
async def update_contact(
        contact_id: Annotated[int, Path(title='The id of the contact to update.')],
        contact_to_update: ContactUpdate,
        db: Session = Depends(get_db)
):
    contact = await contact_repo.update_contact(contact_id, contact_to_update, db)
    if contact:
        return contact
    else:
        raise HTTPException(status_code=404, detail=f'Contact with id {contact_id} not found.')
