import jwt
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.api.models import Organization, UserCreate, OrganizationResponse
from app.api.models.serializer_models import OrganizationCreate
from app.api.services import OrganizationService
from app.core.database_config.db import get_db
from app.core.tasks import create_organization_task

router = APIRouter(
    prefix='/organization',
    tags=['Organization']
)


@router.post("/register")
async def register_organization(org: OrganizationCreate, background_tasks: BackgroundTasks):
    """
    This endpoint registers a new organization and starts a background task
    to process the organization registration. An email notification will be
    sent to the admin once the registration is complete.

    Args:
        org (OrganizationCreate): The data to create the organization.
        background_tasks (BackgroundTasks): The background task manager.

    Returns:
        dict: A message indicating that the registration is in progress.
    """
    # Start background task to create organization
    background_tasks.add_task(create_organization_task, org)
    return {"message": "Organization registration in progress. Admin will be notified via email."}


@router.get("/by-name", response_model=OrganizationResponse)
async def get_organization_by_name(organization_name: str, db: Session = Depends(get_db)):
    """
    This endpoint allows users to fetch an organization's details by its name.
    If the organization is not found, a 404 error is raised.

    Args:
        organization_name (str): The name of the organization to fetch.
        db (Session): The database session dependency to interact with the database.

    Returns:
        OrganizationResponse: The organization data including ID, name, and admin email.

    Raises:
        HTTPException: If the organization is not found, raises a 404 error.
    """
    # Fetch organization by name
    organization = db.query(Organization).filter(Organization.name == organization_name).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with name '{organization_name}' not found."
        )

    return OrganizationResponse(
        id=organization.id,
        name=organization.name,
        admin_email=organization.admin_user.email  # Assuming `organization.admin` is a relationship
    )


@router.post("/create-user")
async def create_user(request: UserCreate, db: Session = Depends(get_db)):
    """
    This endpoint allows the creation of a new user within the organization
    based on the provided user details. If the user cannot be created,
    a 403 error is raised.

    Args:
        request (UserCreate): The user creation request with email and other user data.
        db (Session): The database session dependency to interact with the database.

    Returns:
        dict: A success message with the created user's email and organization name.

    Raises:
        HTTPException: If the user creation fails, raises a 403 error.
    """
    admin_user = OrganizationService().execute(request, db)
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not able to create user with email '{request.user.email}'."
        )
    return {"message": f"User {request.user_email} created successfully in organization."}
