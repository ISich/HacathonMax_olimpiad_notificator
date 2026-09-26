from sqlalchemy import select

from app.models.subject import Subject


class SubjectRepository:

    def __init__(self, session):
        self.session = session

    def get(self, subject_id):
        return self.session.get(Subject, subject_id)

    def get_by_code(self, code: str) -> Subject | None:
        return self.session.scalar(
            select(Subject).where(
                Subject.code == code
            )
        )

    def get_by_name(self, name: str) -> Subject | None:
        return self.session.scalar(
            select(Subject).where(
                Subject.name == name
            )
        )

    def get_all(self) -> list[Subject]:
        return list(
            self.session.scalars(
                select(Subject).order_by(Subject.name)
            ).all()
        )

    def add(self, subject: Subject):
        self.session.add(subject)
        return subject