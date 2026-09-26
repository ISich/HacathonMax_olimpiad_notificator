from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.olympiad import Olympiad, olympiad_grades
from app.models.subject import Subject


class OlympiadRepository:

    def __init__(self, session):
        self.session = session

    def get(self, olympiad_id):
        return self.session.scalar(
            select(Olympiad)
            .where(Olympiad.id == olympiad_id)
            .options(
                selectinload(Olympiad.subjects),
                selectinload(Olympiad.stages),
            )
        )

    def get_by_external_id(
        self,
        external_id: str
    ) -> Olympiad | None:

        return self.session.scalar(
            select(Olympiad).where(
                Olympiad.external_id == external_id
            )
        )

    def get_all(self) -> list[Olympiad]:

        return list(
            self.session.scalars(
                select(Olympiad)
                .options(
                    selectinload(Olympiad.subjects),
                    selectinload(Olympiad.stages),
                )
                .order_by(Olympiad.name)
            ).all()
        )

    def add(self, olympiad: Olympiad):
        self.session.add(olympiad)
        return olympiad

    def find_matching(
            self,
            grade: int,
            subject_codes: set[str],
            levels: set[int] | None = None,
    ) -> list[Olympiad]:
        query = (
            select(Olympiad)
            .join(
                olympiad_grades,
                olympiad_grades.c.olympiad_id == Olympiad.id
            )
            .join(Olympiad.subjects)
            .where(
                olympiad_grades.c.grade == grade,
                Subject.code.in_(subject_codes),
            )
            .options(
                selectinload(Olympiad.subjects),
                selectinload(Olympiad.stages),
            )
            .distinct()
            .order_by(Olympiad.name)
        )

        if levels:
            query = query.where(
                Olympiad.level.in_(levels)
            )

        return list(
            self.session.scalars(query).all()
        )