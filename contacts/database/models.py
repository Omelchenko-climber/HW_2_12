from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func

from contacts.database.db import Base, engine


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    name = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    additional_data = Column(String(255), default=None, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    refresh_token = Column(String(250), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())



Base.metadata.create_all(bind=engine)
