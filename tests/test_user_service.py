from app.repositories.user_repository import UserRepository
from app.services.user_servics import UserService


def create_service():
    repository = UserRepository()
    return UserService(repository)


def test_set_grade():
    service = create_service()

    service.set_grade(123, 9)

    user = service.get_user(123)

    assert user.grade == 9


def test_toggle_subject_add():
    service = create_service()

    service.toggle_subject(123, "math")

    user = service.get_user(123)

    assert "math" in user.subjects


def test_toggle_subject_remove():
    service = create_service()

    service.toggle_subject(123, "math")
    service.toggle_subject(123, "math")

    user = service.get_user(123)

    assert "math" not in user.subjects


def test_toggle_level():
    service = create_service()

    service.toggle_level(123, 1)

    user = service.get_user(123)

    assert 1 in user.selected_levels


def test_clear_olympiads():
    service = create_service()

    user = service.get_or_create_user(123)
    user.olympiads.add(100)
    user.olympiads.add(200)

    service.clear_olympiads(123)

    assert user.olympiads == set()


def test_removed_subjects():
    service = create_service()

    service.toggle_subject(123, "math")
    service.toggle_subject(123, "informatics")

    service.start_subjects_edit(123)

    service.toggle_subject(123, "informatics")
    service.toggle_subject(123, "physics")

    removed = service.get_removed_subjects(123)

    assert removed == {"informatics"}


def test_finish_edit():
    service = create_service()

    service.toggle_subject(123, "math")
    service.start_subjects_edit(123)

    service.finish_edit(123)

    user = service.get_user(123)

    assert user.edit_mode is None
    assert user.original_subjects == set()

def test_change_grade_clears_olympiads():
    service = create_service()

    user = service.get_or_create_user(123)

    user.grade = 9
    user.olympiads = {100, 200, 300}
    user.edit_mode = "grade"

    service.change_grade(
        user_id=123,
        grade=10
    )

    assert user.grade == 10
    assert user.olympiads == set()
    assert user.edit_mode is None

def test_finish_subjects_edit_returns_removed_subjects():
    service = create_service()

    user = service.get_or_create_user(123)

    user.subjects = {
        "math",
        "informatics",
        "physics"
    }

    service.start_subjects_edit(123)

    service.toggle_subject(
        123,
        "informatics"
    )

    removed = service.finish_subjects_edit(123)

    assert removed == {"informatics"}

def test_finish_subjects_edit_does_not_remove_added_subject():
    service = create_service()

    user = service.get_or_create_user(123)

    user.subjects = {
        "math"
    }

    service.start_subjects_edit(123)

    service.toggle_subject(
        123,
        "physics"
    )

    removed = service.finish_subjects_edit(123)

    assert removed == set()

    assert user.subjects == {
        "math",
        "physics"
    }

def test_subject_edit_does_not_finish_before_done():
    service = create_service()

    user = service.get_or_create_user(123)

    user.subjects = {
        "math",
        "informatics"
    }

    service.start_subjects_edit(123)

    service.toggle_subject(
        123,
        "informatics"
    )

    # Пользователь ещё НЕ нажал "Готово"

    assert user.edit_mode == "subjects"

    assert user.original_subjects == {
        "math",
        "informatics"
    }

    assert user.subjects == {
        "math"
    }