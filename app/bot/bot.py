import time

import requests


class Bot:

    def __init__(
        self,
        max_client,
        message_handler,
        callback_handler,
    ):
        self.max_client = max_client
        self.message_handler = message_handler
        self.callback_handler = callback_handler

        self.marker = None

    def run(self):

        print("Бот запущен. Жду сообщения...")

        while True:

            try:
                data = self.max_client.get_updates(
                    marker=self.marker
                )

                for update in data.get("updates", []):

                    update_type = update.get("update_type")

                    if update_type == "message_created":

                        self.message_handler.handle(
                            update["message"]
                        )

                    elif update_type == "message_callback":

                        self.callback_handler.handle(update)

                self.marker = data.get("marker")

            except requests.RequestException as error:

                print(
                    "Ошибка соединения с MAX API. "
                    f"Повтор через 5 секунд: {error}"
                )

                time.sleep(5)