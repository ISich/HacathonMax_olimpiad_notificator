import uuid

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Integer,
    String,
    Table,
    Column,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


user_subjects = Table(
    "user_subjects",
    Base.metadata,

    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Column(
        "subject_id",
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

user_olympiads = Table(
    "user_olympiads",
    Base.metadata,

    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Column(
        "olympiad_id",
        UUID(as_uuid=True),
        ForeignKey("olympiads.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

class UserSelectedLevel(Base):
    __tablename__ = "user_selected_levels"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    max_user_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    grade: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    edit_mode: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    subjects = relationship(
        "Subject",
        secondary=user_subjects,
    )

    olympiads = relationship(
        "Olympiad",
        secondary=user_olympiads,
    )

    selected_levels = relationship(
        "UserSelectedLevel",
        cascade="all, delete-orphan",
    )