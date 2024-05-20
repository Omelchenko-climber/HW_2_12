from sqlalchemy import Column, Integer, String, Date

from contacts.dependencies import Base, engine


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    additional_data = Column(String)


Base.metadata.create_all(bind=engine)
