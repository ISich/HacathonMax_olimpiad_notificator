from app.config import MAX_TOKEN, MAX_BASE_URL
from app.api.max_client import MaxClient
from app.bot.bot import Bot
from app.bot.handlers import MessageHandler
from app.bot.callback_handlers import CallbackHandler

from app.services.user_servics import UserService
from app.services.olympiad_service import OlympiadService
from app.services.notification_worker import NotificationWorker

from app.repositories.user_repository import UserRepository
from app.repositories.olympiad_repository import OlympiadRepository
from app.repositories.subject_repository import SubjectRepository

from app.database.session import SessionLocal

from app.constants import BOT_COMMANDS


def main():

    max_client = MaxClient(
        token=MAX_TOKEN,
        base_url=MAX_BASE_URL,
        verify_ssl=False
    )

    max_client.set_commands(BOT_COMMANDS)

    notification_worker = NotificationWorker(
        max_client=max_client,
        interval_seconds=3600,
    )

    notification_worker.start()

    # Пока держим одну DB-сессию на время работы бота.
    # Позже перед деплоем сделаем нормальный lifecycle сессий.
    session = SessionLocal()

    user_repository = UserRepository(session)
    subject_repository = SubjectRepository(session)
    olympiad_repository = OlympiadRepository(session)

    user_service = UserService(
        user_repository=user_repository,
        subject_repository=subject_repository
    )

    olympiad_service = OlympiadService(
        olympiad_repository=olympiad_repository
    )

    message_handler = MessageHandler(
        max_client=max_client,
        user_service=user_service
    )

    callback_handler = CallbackHandler(
        max_client=max_client,
        user_service=user_service,
        olympiad_service=olympiad_service
    )

    bot = Bot(
        max_client=max_client,
        message_handler=message_handler,
        callback_handler=callback_handler
    )

    try:
        bot.run()
    finally:
        session.close()


if __name__ == "__main__":
    main()