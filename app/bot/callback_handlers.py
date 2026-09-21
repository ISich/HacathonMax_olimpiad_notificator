class CallbackHandler:

    def __init__(self, max_client, user_service):
        self.max_client = max_client
        self.user_service = user_service

    def handle(self, update):

        callback = update["callback"]

        payload = callback["payload"]
        user_id = callback["user"]["user_id"]
        message_id = update["message"]["body"]["mid"]

        print(f"Callback от {user_id}: {payload}")

        if payload.startswith("grade:"):
            self.handle_grade(
                user_id=user_id,
                message_id=message_id,
                payload=payload
            )

    def handle_grade(
        self,
        user_id,
        message_id,
        payload
    ):

        grade = int(payload.split(":")[1])

        self.user_service.set_grade(
            user_id=user_id,
            grade=grade
        )

        print(
            f"Пользователь {user_id}: "
            f"{self.user_service.get_user(user_id)}"
        )

        self.max_client.edit_message(
            message_id=message_id,
            text=f"✓ Выбран {grade} класс."
        )