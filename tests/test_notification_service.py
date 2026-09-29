from datetime import date
from types import SimpleNamespace

from app.services.notification_service import NotificationService


def test_registration_starts_today():

    today = date(2026, 9, 28)

    stage = SimpleNamespace(
        name="Отборочный этап 1",
        registration_start=today,
        registration_end=date(2026, 10, 10),
        stage_start=None,
        stage_end=None,
    )

    olympiad = SimpleNamespace(
        name="Тестовая олимпиада",
        stages=[stage],
    )

    user = SimpleNamespace(
        olympiads=[olympiad],
    )

    service = NotificationService()

    notifications = service.get_notifications_for_user(
        user=user,
        today=today,
    )

    assert len(notifications) == 1
    assert notifications[0]["type"] == "registration_start"
    assert notifications[0]["olympiad"] is olympiad

def test_registration_deadline_in_three_days():

    today = date(2026, 9, 28)

    stage = SimpleNamespace(
        name="Отборочный этап 1",
        registration_start=date(2026, 9, 20),
        registration_end=date(2026, 10, 1),
        stage_start=None,
        stage_end=None,
    )

    olympiad = SimpleNamespace(
        name="Тестовая олимпиада",
        stages=[stage],
    )

    user = SimpleNamespace(
        olympiads=[olympiad],
    )

    service = NotificationService()

    notifications = service.get_notifications_for_user(
        user=user,
        today=today,
    )

    assert len(notifications) == 1
    assert notifications[0]["type"] == "registration_deadline"


def test_no_notifications():

    today = date(2026, 9, 28)

    stage = SimpleNamespace(
        name="Отборочный этап 1",
        registration_start=date(2026, 9, 20),
        registration_end=date(2026, 10, 10),
        stage_start=None,
        stage_end=None,
    )

    olympiad = SimpleNamespace(
        name="Тестовая олимпиада",
        stages=[stage],
    )

    user = SimpleNamespace(
        olympiads=[olympiad],
    )

    service = NotificationService()

    notifications = service.get_notifications_for_user(
        user=user,
        today=today,
    )

    assert notifications == []


def test_multiple_olympiads():

    today = date(2026, 9, 28)

    first_stage = SimpleNamespace(
        name="Отборочный этап",
        registration_start=today,
        registration_end=date(2026, 10, 10),
        stage_start=None,
        stage_end=None,
    )

    second_stage = SimpleNamespace(
        name="Отборочный этап",
        registration_start=date(2026, 9, 20),
        registration_end=date(2026, 10, 1),
        stage_start=None,
        stage_end=None,
    )

    first_olympiad = SimpleNamespace(
        name="Первая олимпиада",
        stages=[first_stage],
    )

    second_olympiad = SimpleNamespace(
        name="Вторая олимпиада",
        stages=[second_stage],
    )

    user = SimpleNamespace(
        olympiads=[
            first_olympiad,
            second_olympiad,
        ],
    )

    service = NotificationService()

    notifications = service.get_notifications_for_user(
        user=user,
        today=today,
    )

    assert len(notifications) == 2

    types = {
        notification["type"]
        for notification in notifications
    }

    assert types == {
        "registration_start",
        "registration_deadline",
    }

def test_stage_starts_today():

    today = date(2026, 11, 6)

    stage = SimpleNamespace(
        name="Отборочный этап 1",
        registration_start=None,
        registration_end=None,
        stage_start=today,
        stage_end=date(2026, 11, 22),
    )

    olympiad = SimpleNamespace(
        name="Тестовая олимпиада",
        stages=[stage],
    )

    user = SimpleNamespace(
        olympiads=[olympiad],
    )

    service = NotificationService()

    notifications = service.get_notifications_for_user(
        user=user,
        today=today,
    )

    assert len(notifications) == 1
    assert notifications[0]["type"] == "stage_start"
    assert notifications[0]["olympiad"] is olympiad
    assert notifications[0]["stage"] is stage

def test_stage_deadline_in_three_days():

    today = date(2026, 11, 19)

    stage = SimpleNamespace(
        name="Отборочный этап 1",
        registration_start=None,
        registration_end=None,
        stage_start=date(2026, 11, 6),
        stage_end=date(2026, 11, 22),
    )

    olympiad = SimpleNamespace(
        name="Тестовая олимпиада",
        stages=[stage],
    )

    user = SimpleNamespace(
        olympiads=[olympiad],
    )

    service = NotificationService()

    notifications = service.get_notifications_for_user(
        user=user,
        today=today,
    )

    assert len(notifications) == 1
    assert notifications[0]["type"] == "stage_deadline"
    assert notifications[0]["olympiad"] is olympiad
    assert notifications[0]["stage"] is stage