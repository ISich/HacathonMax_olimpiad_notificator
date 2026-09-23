from app.repositories.user_repository import UserRepository


def test_create_user():
    repository = UserRepository()

    user = repository.get_or_create(123)

    assert user.user_id == 123


def test_get_existing_user():
    repository = UserRepository()

    created_user = repository.get_or_create(123)
    received_user = repository.get(123)

    assert received_user is created_user


def test_get_unknown_user():
    repository = UserRepository()

    user = repository.get(999)

    assert user is None