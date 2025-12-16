from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import Organization
from app.api.models.db_models import User
from app.api.models.serializer_models import AdminLogin
from app.core.database_config.db import get_admin_db
from app.core.jwt_token import create_access_token, verify_password

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post("/login")
async def login(request: AdminLogin, db: Session = Depends(get_admin_db)):
    """
    Authenticates an admin user and generates an access token.

    This endpoint is used for admin users to log in by verifying their
    credentials (email and password). If the user is authenticated successfully,
    an access token is generated and returned. The user must also be associated
    with an organization, which is verified during the login process.

    Args:
        request (AdminLogin): The login data containing email and password.
        db (Session): The database session to interact with the database.

    Returns:
        dict: A dictionary containing the `access_token` and the `token_type` (bearer).

    Raises:
        HTTPException:
            - 404 Not Found if the admin user is not found in the database.
            - 404 Not Found if the organization associated with the user is not found.
            - 401 Unauthorized if the password provided does not match the stored password.
    """
    # Retrieve user from the database by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin user not found",
        )

    # Retrieve the organization associated with this user
    organization = db.query(Organization).filter(Organization.admin_user_id == user.id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found for this user.")

    # Verify password
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    # Generate access token for authenticated user
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id, "org_name": organization.name})

    return {"access_token": access_token, "token_type": "bearer"}
