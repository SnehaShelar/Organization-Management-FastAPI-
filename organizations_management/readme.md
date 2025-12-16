
This project demonstrates how to use **FastAPI** with **PostgreSQL** for dynamic database creation per organization and **Redis** for caching or background tasks. It leverages Docker for easy setup and management.

## Features

- **FastAPI** application with endpoints to handle user registration and dynamic database creation.
- **PostgreSQL** for database storage with dynamic database creation for each organization.
- **Docker** and **Docker Compose** to containerize the services.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Docker Commands](#docker-commands)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository

2. Make sure you have Docker and Docker Compose installed on your system.


3. Create a .env file in the root of the project with the following content (you can update values as needed):
    ```
    DB_HOST=postgres
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_PORT=5432
    ```
## Setup
This project uses Docker and Docker Compose to run the services. Here's how to set up everything:

1. Build Docker images and start containers:
    ```
    docker-compose build
    docker-compose up
    ```
### API Sample Request:
1. Register an Organization:
This endpoint allows you to register an organization with its admin user. It will dynamically create a new database for the organization.
    ```
    Endpoint: POST /organization/register
    
    Request Body: {
      "name": "Infosys",
      "admin_email": "admin@example.com",
      "admin_password": "Infosys@123",
      "sector": "IT",
      "type": "Private",
      "phone_number": "1234567890",
      "address": "123 Example St, City, Country"
    }
   
   Response: {
      "message": "Organization ExampleOrg created with its own database."
   }
    ```
### API Endpoints

| Endpoint                                 | Method | Description                                                              | Request Body                                                                                                                                               | Response                                                                                                               |
|------------------------------------------|--------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| **Register Organization**                | POST   | Registers a new organization with its admin user and creates a dynamic database. | ```json { "name": "Infosys", "admin_email": "infosys@mail.in", "admin_password": "Infosys@123", "sector": "IT", "type": "Private", "address": "Mumbai", "phone_number": "9876543210" } ``` | ```json { "message": "Organization registration in progress. Admin will be notified via email." } ``` |
| **Admin User Login**                     | POST   | Admin user login to get an access token.                                | ```json { "email": "infosys@mail.in", "password": "Infosys@123", "org_name": "Infosys" } ```                                                               | ```json { "access_token": "<JWT-TOKEN>", "token_type": "bearer" } ```                                                    |
| **Retrieve Organization**                | GET    | Retrieves the organization based on its name.                            | No body required. Query parameter: `organization_name`                                                                                                     | ```json { "organization_id": 1, "organization_name": "Infosys", "admin_user_id": 1 } ```                               |
| **Create Organization User**             | POST   | Creates a new user for the organization.                                | ```json { "user_email": "isha@infosys.in", "user_password": "Isha@123" } ```                                                                                | ```json { "message": "User isha@infosys.in created successfully in organization infosys@mail.in" } ```                |

 - Swagger Documentation: http://127.0.0.1:8000/docs
#