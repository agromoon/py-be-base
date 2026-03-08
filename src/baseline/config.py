from functools import cached_property

from dotenv import load_dotenv
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "BaselineFastAPIproject"
    debug: bool = False

    database_url: AnyUrl | None = None

    postgres_user: str = "baseline"  # env: POSTGRES_USER
    postgres_password: str = "baseline"  # env: POSTGRES_PASSWORD
    postgres_db: str = "baseline"  # env: POSTGRES_DB
    postgres_host: str = "postgres"  # env: POSTGRES_HOST
    postgres_port: int = 5432  # env: POSTGRES_PORT

    sqlite_db_name: str = "test.db"

    @cached_property
    def db_url(self) -> str:
        """Sync database URL (for Alembic)."""
        if self.database_url is not None:
            return str(self.database_url)

        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @cached_property
    def async_db_url(self) -> str:
        """Async database URL (for app runtime, asyncpg driver)."""
        if self.database_url is not None:
            url = str(self.database_url)
            if url.startswith("postgresql://"):
                return url.replace("postgresql://", "postgresql+asyncpg://", 1)
            if url.startswith("postgresql+psycopg://"):
                return url.replace("postgresql+psycopg://", "postgresql+asyncpg://", 1)
            return url

        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


config = Settings()
