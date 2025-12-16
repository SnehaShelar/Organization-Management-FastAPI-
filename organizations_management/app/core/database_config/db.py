from typing import Generator

from fastapi import HTTPException, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.settings import settings
from app.core.jwt_token import decode_jwt_token

# Global session maker dictionary to store engine connections
session_makers = {}


def get_session_for_org(org_name: str) -> sessionmaker:
    """
    Helper function to retrieve or create a session maker for a given organization.
    """
    org_db_name = f"org_{org_name}"
    if org_db_name not in session_makers:
        # Create a new engine for the organization if it doesn't already exist
        engine = create_engine(f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{org_db_name}")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session_makers[org_db_name] = SessionLocal
    return session_makers[org_db_name]


async def get_admin_db(request: Request) -> Generator[Session, None, None]:
    """
    Get database session for the admin user based on the org_name provided in the request body.
    """
    data = await request.json()
    org_name = data.get("org_name")
    if not org_name:
        raise HTTPException(status_code=401, detail="Organization name is required.")

    # Get session for the given organization
    SessionLocal = get_session_for_org(org_name)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_db(request: Request) -> Generator[Session, None, None]:
    """
    Get database session dynamically based on the JWT token extracted from the request header.
    """
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="JWT token is missing")

    token = token.split(" ")[1]  # Extract token from "Bearer <token>"
    payload = decode_jwt_token(token)

    org_name = payload.get("org_name")
    if not org_name:
        raise HTTPException(status_code=401, detail="Invalid token. Organization name is missing.")

    # Get session for the organization from the token's payload
    SessionLocal = get_session_for_org(org_name)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
