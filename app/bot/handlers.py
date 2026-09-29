from app.bot.keyboards import (
    grade_keyboard,
    profile_keyboard,
    restart_keyboard,
)


class MessageHandler:

    def __init__(self, max_client, user_service):
        self.max_client = max_client
        self.user_service = user_service

    def handle(self, message):

        text = message["body"].get("text", "").strip()
        chat_id = message["recipient"]["chat_id"]
        user_id = message["sender"]["user_id"]

        self.user_service.update_chat_id(
            user_id=user_id,
            chat_id=chat_id,
        )

        print(f"Получено от {user_id}: {text}")

        command = text.lower()

        if command == "/start":
            self.handle_start(
                chat_id=chat_id,
                user_id=user_id,
            )

        elif command == "/profile":
            self.handle_profile(
                chat_id=chat_id,
                user_id=user_id,
            )

        elif command == "/info":
            self.handle_info(
                chat_id=chat_id,
            )

        else:
            self.handle_unknown(chat_id)

    def handle_start(self, chat_id, user_id):

        user = self.user_service.get_user(user_id)

        if user is not None and user.grade is not None:
            self.max_client.send_message(
                chat_id=chat_id,
                text=(
                    "⚠️ Ты уже настроил профиль.\n\n"
                    "Если начать настройку заново, "
                    "текущий класс, предметы и выбранные "
                    "олимпиады будут удалены.\n\n"
                    "Начать заново?"
                ),
                attachments=[restart_keyboard()],
            )
            return

        self.max_client.send_message(
            chat_id=chat_id,
            text=(
                "Привет! 👋\n\n"
                "Я помогу тебе следить за олимпиадами "
                "и не пропускать важные сроки.\n\n"
                "В каком классе ты учишься?"
            ),
            attachments=[grade_keyboard()],
        )

    def handle_info(self, chat_id):

        self.max_client.send_message(
            chat_id=chat_id,
            text=(
                "ℹ️ О боте\n\n"
                "Я помогаю школьникам находить подходящие "
                "олимпиады и следить за важными сроками.\n\n"
                "📌 Команды:\n"
                "/start — начать работу или настроить профиль заново\n"
                "/profile — посмотреть и изменить профиль\n"
                "/info — информация о боте и командах\n\n"
                "🔔 Если ты подпишешься на олимпиаду, "
                "я напомню о начале регистрации и этапов, "
                "а также о приближении сроков их окончания.\n\n"
                "Сейчас в базе доступны олимпиады "
                "по математике и информатике. "
                "Олимпиады по другим предметам появятся позже."
            ),
        )

    def handle_unknown(self, chat_id):

        self.max_client.send_message(
            chat_id=chat_id,
            text=(
                "Не удалось распознать команду.\n\n"
                "Используй /start для начала работы "
                "или /info, чтобы посмотреть список команд."
            ),
        )

    def handle_profile(self, chat_id, user_id):

        user = self.user_service.get_user(user_id)

        if user is None or user.grade is None:
            self.max_client.send_message(
                chat_id=chat_id,
                text=(
                    "Ты ещё не настроил профиль.\n"
                    "Отправь /start, чтобы начать."
                ),
            )
            return

        subject_names = [
            subject.name
            for subject in user.subjects
        ]

        subjects_text = ", ".join(subject_names)

        self.max_client.send_message(
            chat_id=chat_id,
            text=(
                "👤 Твой профиль\n\n"
                f"Класс: {user.grade}\n"
                f"Предметы: {subjects_text}"
            ),
            attachments=[
                profile_keyboard()
            ],
        )