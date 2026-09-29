from app.database.session import SessionLocal
from app.repositories.olympiad_repository import OlympiadRepository
from app.repositories.subject_repository import SubjectRepository
from app.repositories.user_repository import UserRepository


def main():

    with SessionLocal() as session:

        olympiad_repository = OlympiadRepository(session)
        subject_repository = SubjectRepository(session)
        user_repository = UserRepository(session)

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

        print("\nПОЛЬЗОВАТЕЛИ:")

        users = user_repository.get_all_with_olympiads()

        if not users:
            print("Пользователи с chat_id не найдены.")

        for user in users:
            print(
                f"\nMAX user ID: {user.max_user_id}"
                f"\nChat ID: {user.max_chat_id}"
                f"\nКласс: {user.grade}"
            )

            if not user.olympiads:
                print("Сохранённых олимпиад нет.")
                continue

            print("Сохранённые олимпиады:")

            for olympiad in user.olympiads:
                print(
                    f"\n  {olympiad.name}"
                    f" | {olympiad.external_id}"
                )

                if not olympiad.stages:
                    print("    Этапов нет.")
                    continue

                for stage in olympiad.stages:
                    print(
                        f"    {stage.name}"
                        f" | регистрация: "
                        f"{stage.registration_start}"
                        f" — {stage.registration_end}"
                        f" | этап: "
                        f"{stage.stage_start}"
                        f" — {stage.stage_end}"
                    )

if __name__ == "__main__":
    main()