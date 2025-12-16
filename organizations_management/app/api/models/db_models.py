from email.policy import default

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    This model stores information about a user, including their email,
    password, and role. The user can be an admin of an organization or
    a regular user, depending on the role.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

    # Relationship with Organization: An admin user can have one associated organization
    organization = relationship('Organization', back_populates='admin_user', uselist=False)


class Organization(Base):
    """
    This model stores details about an organization, such as its name,
    contact details, and the admin user who manages it. Each organization
    must have an admin user associated with it.
    """
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    admin_user_id = Column(Integer, ForeignKey('users.id'))
    sector = Column(String)
    type = Column(String)
    phone_number = Column(String)
    address = Column(String)

    # Relationship with User: An organization has one admin user (admin_user_id is a foreign key to users.id)
    admin_user = relationship('User', back_populates='organization')


# Add the back_populates argument to the User model:
User.organization = relationship('Organization', back_populates='admin_user', uselist=False)
