from app.database.session import SessionLocal
from app.repositories.olympiad_repository import OlympiadRepository
from app.repositories.subject_repository import SubjectRepository


def main():

    with SessionLocal() as session:

        olympiad_repository = OlympiadRepository(session)
        subject_repository = SubjectRepository(session)

        subjects = subject_repository.get_all()
        olympiads = olympiad_repository.get_all()

        print("\nПРЕДМЕТЫ:")

        for subject in subjects:
            print(
                subject.id,
                subject.code,
                subject.name
            )

        print("\nОЛИМПИАДЫ:")

        for olympiad in olympiads:

            subjects_text = ", ".join(
                subject.name
                for subject in olympiad.subjects
            )

            print(
                olympiad.external_id,
                "|",
                olympiad.name,
                "| уровень:",
                olympiad.level,
                "| предметы:",
                subjects_text
            )

        print("\nПОДХОДЯЩИЕ ОЛИМПИАДЫ:")

        matching = olympiad_repository.find_matching(
            grade=8,
            subject_codes={"math", "informatics"},
        )

        for olympiad in matching:

            subjects_text = ", ".join(
                subject.name
                for subject in olympiad.subjects
            )

            print(
                olympiad.name,
                "| уровень:",
                olympiad.level,
                "| предметы:",
                subjects_text
            )

        print("\nПОДХОДЯЩИЕ ОЛИМПИАДЫ I УРОВНЯ:")

        matching_level_1 = olympiad_repository.find_matching(
            grade=8,
            subject_codes={"math", "informatics"},
            levels={1},
        )

        for olympiad in matching_level_1:
            print(
                olympiad.name,
                "| уровень:",
                olympiad.level,
                "| предметы:",
                ", ".join(
                    subject.name
                    for subject in olympiad.subjects
                )
            )


if __name__ == "__main__":
    main()