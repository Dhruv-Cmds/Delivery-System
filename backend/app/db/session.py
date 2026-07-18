import os 

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)

from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from urllib.parse import quote_plus

from app.core import ENV

load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(
    os.getenv("DB_PASSWORD") or ""
)
DB_NAME = os.getenv("DB_NAME")

DB_HOST = os.getenv("DB_HOST", "mysql-shared")
DB_PORT = os.getenv("DB_PORT", "3306")
REDIS_HOST = os.getenv("REDIS_HOST", "redis-shared")


if not all([DB_USER, DB_HOST, DB_NAME]):

    raise ValueError(
        "Missing database environment variables"
    )


DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine (

    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    echo=False
)


AsyncSessionLocal = sessionmaker (
    
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)
