from dataclasses import dataclass, field


@dataclass
class User:
    user_id: int
    grade: int | None = None
    subjects: set[str] = field(default_factory=set)

    # Временное состояние настройки
    selected_levels: set[int] = field(default_factory=set)

    # Итоговые подписки
    olympiads: set[int] = field(default_factory=set)

    edit_mode: str | None = None
    original_subjects: set[str] = field(default_factory=set)