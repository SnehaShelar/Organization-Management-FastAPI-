import psycopg2
from psycopg2 import connect, sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.settings import settings


def check_database_exists(db_name: str) -> bool:
    """
    Checks if the specified database exists in PostgreSQL.

    This function connects to the default "postgres" database and checks
    if the given `db_name` exists in the `pg_database` system table.
    """
    try:
        with connect(
                dbname='postgres',
                user=settings.db_user,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
                    [db_name]
                )
                return cur.fetchone() is not None
    except Exception as e:
        print(f"Error checking database existence: {e}")
        return False


def create_database(db_name: str) -> bool:
    """
    Creates a new database in PostgreSQL.

    This function connects to the default "postgres" database and attempts
    to create a new database with the specified `db_name`. The function
    uses autocommit to ensure the operation is performed immediately.
    """
    try:
        # Establish a connection to the default "postgres" database
        conn = psycopg2.connect(
            dbname='postgres',
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
        )
        conn.autocommit = True  # Enable autocommit for the database creation command
        cur = conn.cursor()

        # Attempt to create the new database
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

        # Clean up
        cur.close()
        conn.close()
        return True  # Return True if database creation is successful

    except Exception as e:
        print(f"Error creating database {db_name}: {e}")
        return False


def get_organization_session(db_name: str) -> Session:
    """
    Initializes a new SQLAlchemy session for the given database.

    This function creates a SQLAlchemy engine and session for the newly created
    organization database. The session is used to interact with the database.
    """
    try:
        engine = create_engine(
            f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{db_name}")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()  # Return a session object

    except Exception as e:
        print(f"Error initializing session for database {db_name}: {e}")
        raise Exception(f"Could not create session for database {db_name}")  # Raise exception if session creation fails
