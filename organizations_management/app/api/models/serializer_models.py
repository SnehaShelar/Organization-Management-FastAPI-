from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    """
    Model for creating a new organization.
    """
    name: str
    admin_email: str
    admin_password: str
    sector: str
    type: str
    phone_number: str
    address: str


class OrganizationResponse(BaseModel):
    """
    Model for the response returned when fetching organization details.
    """
    id: int
    name: str
    admin_email: str


class AdminLogin(BaseModel):
    """
    Model for the admin login request.
    """
    email: str
    password: str
    org_name: str


class UserCreate(BaseModel):
    """
    Model for creating a new user in an organization.
    """
    user_email: str
    user_password: str
