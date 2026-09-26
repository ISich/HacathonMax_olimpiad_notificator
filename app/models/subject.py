import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )