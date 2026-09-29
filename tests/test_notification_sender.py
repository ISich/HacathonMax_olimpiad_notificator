from datetime import date
from types import SimpleNamespace

from app.services.notification_sender import NotificationSender


class FakeUserRepository:

    def __init__(self, users):
        self.users = users

    def get_all_with_olympiads(self):
        return self.users


class FakeNotificationRepository:

    def __init__(self, already_sent=False):
        self.already_sent = already_sent
        self.added = []

    def exists(
        self,
        user_id,
        olympiad_id,
        stage_id,
        notification_type,
    ):
        if self.already_sent:
            return True

        return any(
            item["user_id"] == user_id
            and item["olympiad_id"] == olympiad_id
            and item["stage_id"] == stage_id
            and item["notification_type"] == notification_type
            for item in self.added
        )

    def add(
        self,
        user_id,
        olympiad_id,
        stage_id,
        notification_type,
    ):
        self.added.append({
            "user_id": user_id,
            "olympiad_id": olympiad_id,
            "stage_id": stage_id,
            "notification_type": notification_type,
        })


class FakeNotificationService:

    def __init__(self, notifications):
        self.notifications = notifications

    def get_notifications_for_user(
        self,
        user,
        today=None,
    ):
        return self.notifications


class FakeMaxClient:

    def __init__(self):
        self.messages = []

    def send_message(
        self,
        chat_id,
        text,
        attachments=None,
    ):
        self.messages.append({
            "chat_id": chat_id,
            "text": text,
        })


def make_test_data():

    stage = SimpleNamespace(
        id="stage-1",
    )

    olympiad = SimpleNamespace(
        id="olympiad-1",
    )

    user = SimpleNamespace(
        id="user-1",
        max_chat_id=123456,
    )

    notification = {
        "type": "stage_start",
        "olympiad": olympiad,
        "stage": stage,
        "text": "Начинается олимпиада",
    }

    return user, notification


def test_notification_is_sent():

    user, notification = make_test_data()

    user_repository = FakeUserRepository([user])

    notification_repository = FakeNotificationRepository(
        already_sent=False
    )

    notification_service = FakeNotificationService(
        [notification]
    )

    max_client = FakeMaxClient()

    sender = NotificationSender(
        user_repository=user_repository,
        notification_repository=notification_repository,
        notification_service=notification_service,
        max_client=max_client,
    )

    sent = sender.send_all(
        today=date(2026, 11, 6)
    )

    assert sent == 1

    assert len(max_client.messages) == 1

    assert max_client.messages[0]["chat_id"] == 123456

    assert (
        max_client.messages[0]["text"]
        == "Начинается олимпиада"
    )

    assert len(notification_repository.added) == 1

    assert (
        notification_repository.added[0]["notification_type"]
        == "stage_start"
    )


def test_already_sent_notification_is_skipped():

    user, notification = make_test_data()

    user_repository = FakeUserRepository([user])

    notification_repository = FakeNotificationRepository(
        already_sent=True
    )

    notification_service = FakeNotificationService(
        [notification]
    )

    max_client = FakeMaxClient()

    sender = NotificationSender(
        user_repository=user_repository,
        notification_repository=notification_repository,
        notification_service=notification_service,
        max_client=max_client,
    )

    sent = sender.send_all(
        today=date(2026, 11, 6)
    )

    assert sent == 0
    assert max_client.messages == []
    assert notification_repository.added == []


def test_nothing_is_sent_when_no_notifications():

    user, _ = make_test_data()

    user_repository = FakeUserRepository([user])

    notification_repository = FakeNotificationRepository(
        already_sent=False
    )

    notification_service = FakeNotificationService([])

    max_client = FakeMaxClient()

    sender = NotificationSender(
        user_repository=user_repository,
        notification_repository=notification_repository,
        notification_service=notification_service,
        max_client=max_client,
    )

    sent = sender.send_all(
        today=date(2026, 11, 6)
    )

    assert sent == 0
    assert max_client.messages == []
    assert notification_repository.added == []

def test_notification_is_not_sent_twice():

    user, notification = make_test_data()

    user_repository = FakeUserRepository([user])

    notification_repository = FakeNotificationRepository(
        already_sent=False
    )

    notification_service = FakeNotificationService(
        [notification]
    )

    max_client = FakeMaxClient()

    sender = NotificationSender(
        user_repository=user_repository,
        notification_repository=notification_repository,
        notification_service=notification_service,
        max_client=max_client,
    )

    first_sent = sender.send_all(
        today=date(2026, 11, 6)
    )

    second_sent = sender.send_all(
        today=date(2026, 11, 6)
    )

    assert first_sent == 1
    assert second_sent == 0

    assert len(max_client.messages) == 1
    assert len(notification_repository.added) == 1