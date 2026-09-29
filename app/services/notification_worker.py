import threading
import time

from app.database.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.notification_service import NotificationService
from app.services.notification_sender import NotificationSender


class NotificationWorker:

    def __init__(
        self,
        max_client,
        interval_seconds: int = 3600,
    ):
        self.max_client = max_client
        self.interval_seconds = interval_seconds

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

    def start(self):
        self.thread.start()

    def _run(self):

        while True:

            try:
                self._send_notifications()

            except Exception as error:
                print(
                    f"Ошибка фоновой рассылки: {error}"
                )

            time.sleep(self.interval_seconds)

    def _send_notifications(self):

        with SessionLocal() as session:

            user_repository = UserRepository(session)

            notification_repository = (
                NotificationRepository(session)
            )

            notification_service = NotificationService()

            sender = NotificationSender(
                user_repository=user_repository,
                notification_repository=notification_repository,
                notification_service=notification_service,
                max_client=self.max_client,
            )

            sent = sender.send_all()

            print(
                f"Проверка уведомлений завершена. "
                f"Отправлено: {sent}"
            )