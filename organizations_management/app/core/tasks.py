import random

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.models import User, Base, Organization
from app.core.database_config.create_db_service import create_database, check_database_exists, get_organization_session
from app.core.utils import send_otp_email

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes the provided password using bcrypt.

    This function uses the passlib library to hash the password securely using
    the bcrypt algorithm.
    """
    return pwd_context.hash(password)


def create_organization_task(organization):
    """
    Background task to create the organization and its admin user.

    This function creates a new organization by generating a dynamic database,
    creating necessary tables, and setting up an admin user. It also sends an OTP
    to the admin email for verification purposes.
    """
    # Generate a dynamic database name based on the organization name
    org_db_name = f"org_{organization.name}"

    # Attempt to create the new database
    if not create_database(org_db_name):
        return {"message": f"Failed to create database {org_db_name}"}

    # Ensure the database exists after creation
    if not check_database_exists(org_db_name):
        return {"message": f"Database {org_db_name} does not exist."}

    # Start the process of setting up the organization and its data
    try:
        # Get the database session for the new organization's database
        org_db_session = get_organization_session(org_db_name)

        # Create all tables in the new organization database
        Base.metadata.create_all(bind=org_db_session.get_bind())

        # Create the admin user for the organization
        hashed_password = hash_password(organization.admin_password)
        new_user = User(email=organization.admin_email, password=hashed_password, role="admin")
        org_db_session.add(new_user)
        org_db_session.commit()

        # Create a new record for the organization in the database
        new_organization = Organization(
            name=organization.name,
            admin_user_id=new_user.id,
            sector=organization.sector,
            type=organization.type,
            phone_number=organization.phone_number,
            address=organization.address
        )
        org_db_session.add(new_organization)
        org_db_session.commit()

        # Generate and send OTP for the admin email verification
        otp = str(random.randint(100000, 999999))  # OTP with 6 digits
        send_otp_email(organization.admin_email, otp)

        return {
            "message": f"Organization {organization.name} created successfully with admin {organization.admin_email}"}

    except Exception as e:
        # Log error message and return failure response
        print(f"Error during organization setup: {e}")
        return {"message": "An error occurred during organization setup."}
