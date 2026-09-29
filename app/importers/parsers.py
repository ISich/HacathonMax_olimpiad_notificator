import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DateRange:
    start: datetime | None = None
    end: datetime | None = None
    raw_value: str | None = None


def parse_grades(value) -> list[int]:
    """
    Поддерживаем варианты:
    '7–11' -> [7, 8, 9, 10, 11]
    '9-11' -> [9, 10, 11]
    '8-11/СПО' -> [8, 9, 10, 11]
    '8, 10, 11' -> [8, 10, 11]
    10 -> [10]
    """

    if value is None:
        return []

    if isinstance(value, int):
        return [value]

    text = str(value).strip()

    # Приводим разные виды тире к обычному
    text = text.replace("–", "-").replace("—", "-")

    # Отбрасываем пометки вроде "/СПО"
    text = text.split("/")[0].strip()

    # Диапазон классов, например 7-11
    range_match = re.fullmatch(
        r"(\d{1,2})\s*-\s*(\d{1,2})",
        text,
    )

    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))

        return list(range(start, end + 1))

    # Перечисление классов, например 8, 10, 11
    if "," in text:
        return [
            int(part.strip())
            for part in text.split(",")
            if part.strip().isdigit()
        ]

    return [int(text)]


def parse_level(value) -> int | None:

    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    try:
        return int(float(text))
    except (ValueError, TypeError):
        return None


def parse_date_range(value) -> DateRange:
    """
    Поддерживаем основные варианты из таблицы:

    '01.12.2026 - 01.01.2027'
    'До 20.10.2026'
    'С 07.09.2026'
    '11.10.2026'
    '19.10.2026 – 06.11.2026 (до 11:00 НСК)'

    Если в значении указано несколько конкретных дат,
    используем самую раннюю как начало и самую позднюю
    как окончание.

    Значения без конкретных дат, например:
    'Февраль 2027'
    'Автоматически по результатам отбора'
    'анонсируется позже'

    сохраняются в raw_value.
    """

    if value is None:
        return DateRange()

    if isinstance(value, datetime):
        return DateRange(
            start=value,
            end=value,
        )

    text = str(value).strip()

    if not text:
        return DateRange()

    # Excel/люди могут использовать разные тире
    normalized = (
        text
        .replace("–", "-")
        .replace("—", "-")
    )

    # Ищем все конкретные даты формата ДД.ММ.ГГГГ
    dates = re.findall(
        r"\d{1,2}\.\d{1,2}\.\d{4}",
        normalized,
    )

    parsed_dates = [
        datetime.strptime(date, "%d.%m.%Y")
        for date in dates
    ]

    # До 20.10.2026
    if (
        normalized.lower().startswith("до ")
        and parsed_dates
    ):
        return DateRange(
            end=parsed_dates[0],
            raw_value=text,
        )

    # С 07.09.2026
    if (
        normalized.lower().startswith("с ")
        and parsed_dates
    ):
        return DateRange(
            start=parsed_dates[0],
            raw_value=text,
        )

    # Несколько дат.
    # Берём самую раннюю и самую позднюю.
    if len(parsed_dates) >= 2:
        return DateRange(
            start=min(parsed_dates),
            end=max(parsed_dates),
            raw_value=text,
        )

    # Одна конкретная дата
    if len(parsed_dates) == 1:
        return DateRange(
            start=parsed_dates[0],
            end=parsed_dates[0],
            raw_value=text,
        )

    # Например:
    # "ноябрь 2026"
    # "февраль 2027"
    # "Автоматически по результатам отбора"
    # "анонсируется позже"
    return DateRange(
        raw_value=text,
    )