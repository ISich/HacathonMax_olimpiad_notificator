from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.olympiad import Olympiad
from app.models.subject import Subject


class UserRepository:

    def __init__(self, session):
        self.session = session

    def get(self, max_user_id: int) -> User | None:

        return self.session.scalar(
            select(User)
            .where(User.max_user_id == max_user_id)
            .options(
                selectinload(User.subjects),
                selectinload(User.olympiads),
                selectinload(User.selected_levels),
            )
        )

    def get_or_create(self, max_user_id: int) -> User:

        user = self.get(max_user_id)

        if user is None:
            user = User(
                max_user_id=max_user_id
            )

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

        return user

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def get_all_with_olympiads(self) -> list[User]:
        return list(
            self.session.scalars(
                select(User)
                .options(
                    selectinload(User.olympiads)
                    .selectinload(Olympiad.stages)
                )
            ).all()
        )