from datetime import date


class NotificationSender:

    def __init__(
        self,
        user_repository,
        notification_repository,
        notification_service,
        max_client,
    ):
        self.user_repository = user_repository
        self.notification_repository = notification_repository
        self.notification_service = notification_service
        self.max_client = max_client

    def send_all(
        self,
        today: date | None = None,
    ) -> int:

        users = self.user_repository.get_all_with_olympiads()

        sent = 0

        for user in users:

            notifications = (
                self.notification_service
                .get_notifications_for_user(
                    user=user,
                    today=today,
                )
            )

            for notification in notifications:

                olympiad = notification["olympiad"]
                stage = notification["stage"]
                notification_type = notification["type"]

                already_sent = (
                    self.notification_repository.exists(
                        user_id=user.id,
                        olympiad_id=olympiad.id,
                        stage_id=stage.id,
                        notification_type=notification_type,
                    )
                )

                if already_sent:
                    continue

                self.max_client.send_message(
                    chat_id=user.max_chat_id,
                    text=notification["text"],
                )

                self.notification_repository.add(
                    user_id=user.id,
                    olympiad_id=olympiad.id,
                    stage_id=stage.id,
                    notification_type=notification_type,
                )

                sent += 1

        return sent