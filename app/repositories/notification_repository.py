from sqlalchemy import select

from app.models.notification import NotificationHistory


class NotificationRepository:

    def __init__(self, session):
        self.session = session

    def exists(
        self,
        user_id,
        olympiad_id,
        stage_id,
        notification_type: str,
    ) -> bool:

        notification = self.session.scalar(
            select(NotificationHistory)
            .where(
                NotificationHistory.user_id == user_id,
                NotificationHistory.olympiad_id == olympiad_id,
                NotificationHistory.stage_id == stage_id,
                NotificationHistory.notification_type
                == notification_type,
            )
        )

        return notification is not None

    def add(
        self,
        user_id,
        olympiad_id,
        stage_id,
        notification_type: str,
    ) -> None:

        notification = NotificationHistory(
            user_id=user_id,
            olympiad_id=olympiad_id,
            stage_id=stage_id,
            notification_type=notification_type,
        )

        self.session.add(notification)
        self.session.commit()