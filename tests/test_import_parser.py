from datetime import datetime

from app.importers.parsers import (
    parse_grades,
    parse_level,
    parse_date_range,
)


def test_parse_grades_range():
    assert parse_grades("7–11") == [7, 8, 9, 10, 11]


def test_parse_grades_range_with_dash():
    assert parse_grades("9-11") == [9, 10, 11]


def test_parse_grades_list():
    assert parse_grades("8, 10, 11") == [8, 10, 11]


def test_parse_single_grade():
    assert parse_grades(10) == [10]


def test_parse_level():
    assert parse_level("2") == 2


def test_parse_empty_level():
    assert parse_level(None) is None


def test_parse_date_range():
    result = parse_date_range(
        "01.12.2026 - 01.01.2027"
    )

    assert result.start == datetime(2026, 12, 1)
    assert result.end == datetime(2027, 1, 1)


def test_parse_date_until():
    result = parse_date_range("До 20.10.2026")

    assert result.start is None
    assert result.end == datetime(2026, 10, 20)


def test_parse_date_from():
    result = parse_date_range("С 07.09.2026")

    assert result.start == datetime(2026, 9, 7)
    assert result.end is None


def test_parse_approximate_date():
    result = parse_date_range("ноябрь 2026")

    assert result.start is None
    assert result.end is None
    assert result.raw_value == "ноябрь 2026"


def test_parse_empty_date():
    result = parse_date_range(None)

    assert result.start is None
    assert result.end is None