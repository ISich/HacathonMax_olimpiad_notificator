from app.constants import SUBJECTS
from app.database.session import SessionLocal
from app.importers.olympiad_excel import OlympiadExcelImporter
from app.models.subject import Subject
from app.repositories.olympiad_repository import OlympiadRepository
from app.repositories.subject_repository import SubjectRepository
from app.services.olympiad_import_service import OlympiadImportService


def main():

    with SessionLocal() as session:

        subject_repository = SubjectRepository(session)

        # 1. Добавляем недостающие предметы
        for code, name in SUBJECTS.items():

            subject = subject_repository.get_by_code(code)

            if subject is None:
                subject_repository.add(
                    Subject(
                        code=code,
                        name=name
                    )
                )

        session.commit()

        print("Предметы готовы.")

        # 2. Загружаем олимпиады из Excel
        importer = OlympiadExcelImporter(
            "data/OlimpiadData.xlsx"
        )

        rows = importer.read()

        olympiad_repository = OlympiadRepository(session)

        service = OlympiadImportService(
            session=session,
            olympiad_repository=olympiad_repository,
            subject_repository=subject_repository,
        )

        imported = service.import_rows(rows)

        print(f"Олимпиады готовы. Обработано: {imported}")


if __name__ == "__main__":
    main()