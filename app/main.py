from app.config import MAX_TOKEN, MAX_BASE_URL
from app.api.max_client import MaxClient
from app.bot.bot import Bot
from app.bot.handlers import MessageHandler
from app.bot.callback_handlers import CallbackHandler
from app.services.user_servics import UserService
from app.constants import BOT_COMMANDS
from app.repositories.user_repository import UserRepository


def main():

    max_client = MaxClient(
        token=MAX_TOKEN,
        base_url=MAX_BASE_URL,
        verify_ssl=False
    )

    max_client.set_commands(BOT_COMMANDS)

    user_repository = UserRepository()

    user_service = UserService(
        user_repository=user_repository
    )

    message_handler = MessageHandler(
        max_client=max_client,
        user_service=user_service
    )

    callback_handler = CallbackHandler(
        max_client=max_client,
        user_service=user_service
    )

    bot = Bot(
        max_client=max_client,
        message_handler=message_handler,
        callback_handler=callback_handler
    )

    bot.run()


if __name__ == "__main__":
    main()