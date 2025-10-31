import os
import reflex as rx


def get_database_url():
    """Get the appropriate database URL for the environment."""
    db_url = os.getenv("REFLEX_DB_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return db_url


def get_async_database_url():
    """Get the async database URL for the environment."""
    db_url = os.getenv("REFLEX_ASYNC_DB_URL") or os.getenv("REFLEX_DB_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif db_url and db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return db_url