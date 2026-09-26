from app.database.session import SessionLocal
from app.importers.olympiad_excel import OlympiadExcelImporter
from app.repositories.olympiad_repository import OlympiadRepository
from app.repositories.subject_repository import SubjectRepository
from app.services.olympiad_import_service import OlympiadImportService


def main():
    importer = OlympiadExcelImporter(
        "data/OlimpiadData.xlsx"
    )

    rows = importer.read()

    print(f"Найдено олимпиад: {len(rows)}")

    with SessionLocal() as session:
        olympiad_repository = OlympiadRepository(session)
        subject_repository = SubjectRepository(session)

        service = OlympiadImportService(
            session=session,
            olympiad_repository=olympiad_repository,
            subject_repository=subject_repository,
        )

        imported = service.import_rows(rows)

    print(f"Импортировано: {imported}")


if __name__ == "__main__":
    main()