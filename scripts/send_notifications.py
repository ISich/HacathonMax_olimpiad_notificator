from app.api.max_client import MaxClient
from app.config import MAX_TOKEN, MAX_BASE_URL
from app.database.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.notification_sender import NotificationSender
from app.services.notification_service import NotificationService
#from datetime import date


def main():
    max_client = MaxClient(
        token=MAX_TOKEN,
        base_url=MAX_BASE_URL,
        verify_ssl=False,
    )

    with SessionLocal() as session:
        user_repository = UserRepository(session)

        notification_repository = NotificationRepository(
            session
        )

        notification_service = NotificationService()

        sender = NotificationSender(
            user_repository=user_repository,
            notification_repository=notification_repository,
            notification_service=notification_service,
            max_client=max_client,
        )

        sent = sender.send_all()
        #sent = sender.send_all(today=date(2026, 11, 6))

        print(
            f"Отправлено уведомлений: {sent}"
        )


if __name__ == "__main__":
    main()