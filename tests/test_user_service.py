from app.repositories.user_repository import UserRepository
from app.services.user_servics import UserService
from app.models.subject import Subject
from app.repositories.subject_repository import SubjectRepository
from app.models.olympiad import Olympiad


def create_service(db_session):

    user_repository = UserRepository(db_session)
    subject_repository = SubjectRepository(db_session)

    # Предметы, необходимые тестам
    subjects = [
        Subject(
            code="math",
            name="Математика"
        ),
        Subject(
            code="informatics",
            name="Информатика"
        ),
        Subject(
            code="physics",
            name="Физика"
        ),
    ]

    db_session.add_all(subjects)
    db_session.commit()

    return UserService(
        user_repository=user_repository,
        subject_repository=subject_repository,
    )


def test_set_grade(db_session):
    service = create_service(db_session)

    service.set_grade(123, 9)

    user = service.get_user(123)

    assert user.grade == 9


def test_toggle_subject_add(db_session):
    service = create_service(db_session)

    service.toggle_subject(123, "math")

    assert service.get_subjects(123) == {"math"}


def test_toggle_subject_remove(db_session):
    service = create_service(db_session)

    service.toggle_subject(123, "math")
    service.toggle_subject(123, "math")

    assert service.get_subjects(123) == set()


def test_toggle_level(db_session):
    service = create_service(db_session)

    service.toggle_level(123, 1)

    assert service.get_selected_levels(123) == {1}


def test_clear_olympiads(db_session):
    service = create_service(db_session)

    user = service.get_or_create_user(123)

    olympiad_1 = Olympiad(
        external_id="test-1",
        name="Тестовая олимпиада 1",
    )

    olympiad_2 = Olympiad(
        external_id="test-2",
        name="Тестовая олимпиада 2",
    )

    db_session.add_all([
        olympiad_1,
        olympiad_2,
    ])

    user.olympiads.extend([
        olympiad_1,
        olympiad_2,
    ])

    db_session.commit()

    service.clear_olympiads(123)

    assert user.olympiads == []


def test_finish_edit(db_session):
    service = create_service(db_session)

    service.start_subjects_edit(123)
    service.finish_edit(123)

    user = service.get_user(123)

    assert user.edit_mode is None

def test_change_grade_clears_olympiads(db_session):
    service = create_service(db_session)

    user = service.get_or_create_user(123)

    olympiad_1 = Olympiad(
        external_id="test-1",
        name="Тестовая олимпиада 1",
    )

    olympiad_2 = Olympiad(
        external_id="test-2",
        name="Тестовая олимпиада 2",
    )

    db_session.add_all([
        olympiad_1,
        olympiad_2,
    ])

    user.grade = 9
    user.olympiads.extend([
        olympiad_1,
        olympiad_2,
    ])
    user.edit_mode = "grade"

    db_session.commit()

    service.change_grade(
        user_id=123,
        grade=10
    )

    assert user.grade == 10
    assert user.olympiads == []
    assert user.edit_mode is None

def test_subject_edit_does_not_finish_before_done(db_session):
    service = create_service(db_session)

    service.start_subjects_edit(123)

    service.toggle_subject(
        123,
        "math"
    )

    user = service.get_user(123)

    assert user.edit_mode == "subjects"
    assert service.get_subjects(123) == {"math"}

def test_remove_irrelevant_olympiads(db_session):
    service = create_service(db_session)

    user = service.get_or_create_user(123)

    # Выбираем два предмета
    service.toggle_subject(123, "math")
    service.toggle_subject(123, "informatics")

    # Берём предметы из БД
    math = next(
        subject
        for subject in user.subjects
        if subject.code == "math"
    )

    informatics = next(
        subject
        for subject in user.subjects
        if subject.code == "informatics"
    )

    # Создаём две олимпиады
    from app.models.olympiad import Olympiad

    math_olympiad = Olympiad(
        external_id="test_math",
        name="Олимпиада по математике",
        subjects=[math],
    )

    informatics_olympiad = Olympiad(
        external_id="test_informatics",
        name="Олимпиада по информатике",
        subjects=[informatics],
    )

    db_session.add_all([
        math_olympiad,
        informatics_olympiad,
    ])
    db_session.commit()

    # Подписываем пользователя на обе
    service.set_olympiads(
        123,
        [math_olympiad, informatics_olympiad]
    )

    # Пользователь убирает информатику
    service.toggle_subject(
        123,
        "informatics"
    )

    # Удаляем олимпиады по больше не выбранным предметам
    service.remove_irrelevant_olympiads(123)

    assert len(user.olympiads) == 1
    assert user.olympiads[0].name == "Олимпиада по математике"