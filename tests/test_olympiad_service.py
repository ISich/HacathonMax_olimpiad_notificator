from app.models.olympiad import Olympiad, olympiad_grades
from app.models.subject import Subject
from app.repositories.olympiad_repository import OlympiadRepository
from app.services.olympiad_service import OlympiadService


def create_service(db_session):

    math = Subject(
        code="math",
        name="Математика",
    )

    informatics = Subject(
        code="informatics",
        name="Информатика",
    )

    physics = Subject(
        code="physics",
        name="Физика",
    )

    olympiad_math = Olympiad(
        external_id="test-math",
        name="Тестовая математика",
        level=1,
        subjects=[math],
    )

    olympiad_informatics = Olympiad(
        external_id="test-informatics",
        name="Тестовая информатика",
        level=2,
        subjects=[informatics],
    )

    olympiad_physics = Olympiad(
        external_id="test-physics",
        name="Тестовая физика",
        level=1,
        subjects=[physics],
    )

    db_session.add_all([
        math,
        informatics,
        physics,
        olympiad_math,
        olympiad_informatics,
        olympiad_physics,
    ])

    db_session.flush()

    # Классы олимпиад
    db_session.execute(
        olympiad_grades.insert(),
        [
            {"olympiad_id": olympiad_math.id, "grade": 9},
            {"olympiad_id": olympiad_math.id, "grade": 10},

            {"olympiad_id": olympiad_informatics.id, "grade": 9},

            {"olympiad_id": olympiad_physics.id, "grade": 10},
        ]
    )

    db_session.commit()

    service = OlympiadService(
        olympiad_repository=OlympiadRepository(db_session)
    )

    return service


def test_find_by_grade_and_subject(db_session):
    service = create_service(db_session)

    result = service.find_for_user(
        grade=9,
        subject_codes={"math"}
    )

    assert len(result) == 1
    assert result[0].external_id == "test-math"


def test_wrong_grade_not_found(db_session):
    service = create_service(db_session)

    result = service.find_for_user(
        grade=8,
        subject_codes={"informatics"}
    )

    assert result == []


def test_filter_by_level(db_session):
    service = create_service(db_session)

    result = service.find_for_user(
        grade=9,
        subject_codes={
            "math",
            "informatics"
        },
        levels={2}
    )

    assert len(result) == 1
    assert result[0].external_id == "test-informatics"


def test_multiple_subjects(db_session):
    service = create_service(db_session)

    result = service.find_for_user(
        grade=10,
        subject_codes={
            "math",
            "physics"
        }
    )

    external_ids = {
        olympiad.external_id
        for olympiad in result
    }

    assert external_ids == {
        "test-math",
        "test-physics"
    }