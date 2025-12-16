from fastapi import HTTPException

from app.api.models import User
from app.core.tasks import hash_password


class OrganizationService:

    def execute(self, request, db):
        """
        Creates a new user in the database for the organization.

        This method creates a new user in the organization, hashes the user's
        password before storing it, and saves the user to the database. If there
        is any issue during the database transaction, it rolls back and raises
        an HTTP exception with a 500 status code.
        """
        hashed_password = hash_password(request.user_password)
        new_user = User(email=request.user_email, password=hashed_password)

        try:
            # Add and commit the new user to the database
            db.add(new_user)
            db.commit()
        except Exception as e:
            # Rollback the transaction in case of any error
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create user.")

        return new_user
