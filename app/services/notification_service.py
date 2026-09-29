from datetime import date, datetime, timedelta


class NotificationService:

    @staticmethod
    def _to_date(value):
        if value is None:
            return None

        if isinstance(value, datetime):
            return value.date()

        return value

    def get_notifications_for_user(
        self,
        user,
        today: date | None = None,
    ) -> list[dict]:

        if today is None:
            today = date.today()

        notifications = []

        for olympiad in user.olympiads:
            subjects_text = ", ".join(
                subject.name
                for subject in olympiad.subjects
            )
            for stage in olympiad.stages:

                registration_start = self._to_date(
                    stage.registration_start
                )

                registration_end = self._to_date(
                    stage.registration_end
                )

                if registration_start == today:
                    notifications.append({
                        "type": "registration_start",
                        "olympiad": olympiad,
                        "stage": stage,
                        "text": (
                            "📅 Сегодня начинается регистрация!\n\n"
                            f"🏆 {olympiad.name}\n"
                            f"📚 {subjects_text}\n"
                            f"Этап: {stage.name}"
                        ),
                    })

                if (
                    registration_end is not None
                    and registration_end - today
                    == timedelta(days=3)
                ):
                    notifications.append({
                        "type": "registration_deadline",
                        "olympiad": olympiad,
                        "stage": stage,
                        "text": (
                            "⏰ До окончания регистрации "
                            "осталось 3 дня!\n\n"
                            f"🏆 {olympiad.name}\n"
                            f"📚 {subjects_text}\n"
                            f"Этап: {stage.name}\n"
                            f"Регистрация до: "
                            f"{registration_end:%d.%m.%Y}"
                        ),
                    })

                stage_start = self._to_date(
                    stage.stage_start
                )

                stage_end = self._to_date(
                    stage.stage_end
                )

                if stage_start == today:
                    notifications.append({
                        "type": "stage_start",
                        "olympiad": olympiad,
                        "stage": stage,
                        "text": (
                            "🚀 Сегодня начинается этап олимпиады!\n\n"
                            f"🏆 {olympiad.name}\n"
                            f"📚 {subjects_text}\n"
                            f"Этап: {stage.name}"
                        ),
                    })

                if (
                        stage_end is not None
                        and stage_end - today == timedelta(days=3)
                ):
                    notifications.append({
                        "type": "stage_deadline",
                        "olympiad": olympiad,
                        "stage": stage,
                        "text": (
                            "⏰ До окончания этапа осталось 3 дня!\n\n"
                            f"🏆 {olympiad.name}\n"
                            f"📚 {subjects_text}\n"
                            f"Этап: {stage.name}\n"
                            f"Окончание: {stage_end:%d.%m.%Y}"
                        ),
                    })

        return notifications