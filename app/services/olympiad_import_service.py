from sqlalchemy import delete, insert

from app.models.olympiad import (
    Olympiad,
    OlympiadStage,
    olympiad_grades,
)
from app.models.subject import Subject
from app.importers.parsers import (
    parse_grades,
    parse_level,
    parse_date_range,
)


class OlympiadImportService:

    def __init__(
        self,
        session,
        olympiad_repository,
        subject_repository,
    ):
        self.session = session
        self.olympiad_repository = olympiad_repository
        self.subject_repository = subject_repository

    def import_rows(self, rows: list[dict]):

        imported = 0

        try:
            for row in rows:
                self._import_row(row)
                imported += 1

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

        return imported

    def _import_row(self, row: dict):

        external_id = str(row["external_id"]).strip()

        olympiad = (
            self.olympiad_repository
            .get_by_external_id(external_id)
        )

        if olympiad is None:
            olympiad = Olympiad(
                external_id=external_id,
                name=str(row["name"]).strip(),
            )

            self.olympiad_repository.add(olympiad)

            # UUID должен появиться до вставки grades
            self.session.flush()

        # Обновляем основные данные
        olympiad.name = str(row["name"]).strip()
        olympiad.level = parse_level(row.get("level"))
        olympiad.organizer = self._clean(row.get("organizer"))
        olympiad.website = self._clean(row.get("website"))
        olympiad.notes = self._clean(row.get("notes"))

        self._set_subject(
            olympiad,
            row.get("subject")
        )

        self._set_grades(
            olympiad,
            row.get("grades")
        )

        self._set_stages(
            olympiad,
            row
        )

    def _set_subject(self, olympiad, value):

        if value is None:
            olympiad.subjects = []
            return

        subject_name = str(value).strip()

        subject = self.subject_repository.get_by_name(
            subject_name
        )

        if subject is None:
            subject = Subject(
                code=self._make_subject_code(subject_name),
                name=subject_name,
            )

            self.subject_repository.add(subject)
            self.session.flush()

        olympiad.subjects = [subject]

    def _set_grades(self, olympiad, value):

        grades = parse_grades(value)

        self.session.execute(
            delete(olympiad_grades).where(
                olympiad_grades.c.olympiad_id
                == olympiad.id
            )
        )

        if grades:
            self.session.execute(
                insert(olympiad_grades),
                [
                    {
                        "olympiad_id": olympiad.id,
                        "grade": grade,
                    }
                    for grade in grades
                ]
            )

    def _set_stages(self, olympiad, row):

        olympiad.stages.clear()

        stage_definitions = [
            (
                "Отборочный этап 1",
                "qualification_registration",
                "qualification_stage_1",
            ),
            (
                "Отборочный этап 2",
                None,
                "qualification_stage_2",
            ),
            (
                "Отборочный этап 3",
                None,
                "qualification_stage_3",
            ),
            (
                "Финал",
                "final_registration",
                "final_stage",
            ),
        ]

        for name, registration_key, stage_key in stage_definitions:

            registration = (
                parse_date_range(row.get(registration_key))
                if registration_key
                else None
            )

            stage = parse_date_range(
                row.get(stage_key)
            )

            if (
                registration is None
                and stage.start is None
                and stage.end is None
                and stage.raw_value is None
            ):
                continue

            olympiad.stages.append(
                OlympiadStage(
                    name=name,

                    registration_start=(
                        registration.start
                        if registration
                        else None
                    ),

                    registration_end=(
                        registration.end
                        if registration
                        else None
                    ),

                    stage_start=stage.start,
                    stage_end=stage.end,

                    raw_value=stage.raw_value,
                )
            )

    @staticmethod
    def _clean(value):

        if value is None:
            return None

        value = str(value).strip()

        return value or None

    @staticmethod
    def _make_subject_code(name: str):

        replacements = {
            "Математика": "math",
            "Информатика": "informatics",
            "Физика": "physics",
            "Химия": "chemistry",
            "Биология": "biology",
            "Русский язык": "russian",
            "Астрономия": "astronomy",
            "Экономика": "economics",
        }

        return replacements.get(
            name,
            name.lower()
                .replace(" ", "_")
        )