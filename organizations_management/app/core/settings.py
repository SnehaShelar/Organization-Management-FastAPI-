from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate the settings to access the configuration
settings = Settings()
