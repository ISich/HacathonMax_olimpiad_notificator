from app.repositories.user_repository import UserRepository


def test_create_user(db_session):
    repository = UserRepository(db_session)

    user = repository.get_or_create(123)

    assert user.max_user_id == 123


def test_get_existing_user(db_session):
    repository = UserRepository(db_session)

    created_user = repository.get_or_create(123)
    received_user = repository.get(123)

    assert received_user is created_user


def test_get_unknown_user(db_session):
    repository = UserRepository(db_session)

    user = repository.get(999)

    assert user is None