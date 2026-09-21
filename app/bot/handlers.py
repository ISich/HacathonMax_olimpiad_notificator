from app.bot.keyboards import grade_keyboard


class MessageHandler:

    def __init__(self, max_client, user_service):

        self.max_client = max_client
        self.user_service = user_service

    def handle(self, message):

        text = message["body"].get("text", "")
        chat_id = message["recipient"]["chat_id"]
        user_id = message["sender"]["user_id"]

        print(f"Получено от {user_id}: {text}")

        if text.lower() == "/start":
            self.handle_start(chat_id)

        else:
            self.handle_unknown(chat_id)

    def handle_start(self, chat_id):

        self.max_client.send_message(
            chat_id=chat_id,
            text=(
                "Привет! 👋\n\n"
                "Я помогу тебе следить за олимпиадами "
                "и не пропускать важные сроки.\n\n"
                "В каком классе ты учишься?"
            ),
            attachments=[grade_keyboard()]
        )

    def handle_unknown(self, chat_id):

        self.max_client.send_message(
            chat_id=chat_id,
            text="Для начала работы отправь /start"
        )