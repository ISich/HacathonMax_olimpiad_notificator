import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    Column,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


olympiad_subjects = Table(
    "olympiad_subjects",
    Base.metadata,

    Column(
        "olympiad_id",
        UUID(as_uuid=True),
        ForeignKey("olympiads.id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Column(
        "subject_id",
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


olympiad_grades = Table(
    "olympiad_grades",
    Base.metadata,

    Column(
        "olympiad_id",
        UUID(as_uuid=True),
        ForeignKey("olympiads.id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Column(
        "grade",
        Integer,
        primary_key=True,
    ),
)


class Olympiad(Base):
    __tablename__ = "olympiads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    level: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    organizer: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    subjects = relationship(
        "Subject",
        secondary=olympiad_subjects,
    )

    stages = relationship(
        "OlympiadStage",
        back_populates="olympiad",
        cascade="all, delete-orphan",
    )



class OlympiadStage(Base):
    __tablename__ = "olympiad_stages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    olympiad_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("olympiads.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    registration_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    registration_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    stage_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    stage_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    raw_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    olympiad = relationship(
        "Olympiad",
        back_populates="stages",
    )