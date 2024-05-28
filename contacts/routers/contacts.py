from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..schemas import ContactBase, ContactUpdate, ContactResponse, ContactCreate
from contacts.database.db import get_db
from contacts.database.models import Contact, User
from ..repository import contact_repo
from ..services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/upcoming_birthdays')
async def get_upcoming_birthdays(
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    contacts = await contact_repo.get_upcoming_birthdays_from_db(current_user, db)

    return contacts


@router.get('/search')
async def search_contact(
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db),
        name: Annotated[str | None, Query(alias='name')] = None,
        surname: Annotated[str | None, Query(alias='surname')] = None,
        email: Annotated[str | None, Query(alias='email')] = None
):
    contact = await contact_repo. search_contact(current_user, db, name, surname, email)

    return contact


@router.get('/get_one/{contact_id}', response_model=ContactResponse)
async def get_contact(
        contact_id: Annotated[int, Path(title='The id of the contact to get')],
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    contact = await contact_repo.get_contact(contact_id, current_user, db)

    return contact


@router.get('/all', response_model=list[ContactResponse])
async def all_contacts(
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
) -> list[ContactBase]:
    contacts = await contact_repo.get_all_contacts(current_user, db)

    return contacts


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_new_contact(
        contact: ContactCreate,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):

    try:
        contact = await contact_repo.add_contact(contact, current_user, db)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=repr(e))

    return contact


@router.delete('/delete/{contact_id}')
async def delete_contact(
        contact_id: Annotated[int, Path(title='The id of the contact to delete.')],
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    await contact_repo.delete_contact(contact_id, current_user, db)

    return {'status': f'contact with id {contact_id} was deleted.'}


@router.put('/update/{contact_id}', status_code=status.HTTP_201_CREATED)
async def update_contact(
        contact_id: Annotated[int, Path(title='The id of the contact to update.')],
        contact_to_update: ContactUpdate,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)
):
    contact = await contact_repo.update_contact(contact_id, current_user, contact_to_update, db)
    if contact:
        return contact
    else:
        raise HTTPException(status_code=404, detail=f'Contact with id {contact_id} not found.')
