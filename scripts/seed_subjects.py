from app.constants import SUBJECTS
from app.database.session import SessionLocal
from app.models.subject import Subject
from app.repositories.subject_repository import SubjectRepository


def main():

    with SessionLocal() as session:

        repository = SubjectRepository(session)

        added = 0

        for code, name in SUBJECTS.items():

            subject = repository.get_by_code(code)

            if subject is None:
                repository.add(
                    Subject(
                        code=code,
                        name=name
                    )
                )
                added += 1

        session.commit()

        print(f"Добавлено предметов: {added}")


if __name__ == "__main__":
    main()