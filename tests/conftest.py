import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import TEST_DATABASE_URL
from app.database.base import Base

# Импортируем модели, чтобы они были зарегистрированы в Base.metadata
from app.models.subject import Subject
from app.models.olympiad import Olympiad, OlympiadStage
from app.models.user import User, UserSelectedLevel


if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL не указан в .env")

if "olympiad_bot_test" not in TEST_DATABASE_URL:
    raise RuntimeError(
        "Тесты разрешено запускать только на olympiad_bot_test"
    )


engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture
def db_session():
    # Перед каждым тестом создаём чистую структуру
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()

        Base.metadata.drop_all(engine)