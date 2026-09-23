from app.bot.keyboards import (
    subjects_keyboard,
    olympiad_selection_keyboard,
    levels_keyboard,
    grade_keyboard
)
from app.constants import SUBJECTS


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

        elif payload.startswith("subject:"):
            self.handle_subject(
                user_id=user_id,
                message_id=message_id,
                payload=payload
            )

        elif payload == "subjects:done":
            self.handle_subjects_done(
                user_id=user_id,
                message_id=message_id
            )

        elif payload == "olympiads:all":
            self.handle_all_olympiads(
                user_id=user_id,
                message_id=message_id
            )

        elif payload == "olympiads:levels":
            self.handle_levels_start(
                user_id=user_id,
                message_id=message_id
            )

        elif payload == "olympiads:specific":
            self.handle_specific_olympiads(
                message_id=message_id
            )

        elif payload == "profile:grade":
            self.handle_profile_grade(
                user_id=user_id,
                message_id=message_id
            )

        elif payload == "profile:subjects":
            self.handle_profile_subjects(
                user_id=user_id,
                message_id=message_id
            )

        elif payload == "profile:olympiads":
            self.handle_profile_olympiads(
                user_id=user_id,
                message_id=message_id
            )

        elif payload.startswith("level:"):
            self.handle_level(
                user_id=user_id,
                message_id=message_id,
                payload=payload
            )

        elif payload == "levels:done":
            self.handle_levels_done(
                user_id=user_id,
                message_id=message_id
            )

    def handle_grade(self, user_id, message_id, payload):

        grade = int(payload.split(":")[1])

        user = self.user_service.get_or_create_user(user_id)

        # Изменение класса из профиля
        if user.edit_mode == "grade":
            self.user_service.change_grade(
                user_id=user_id,
                grade=grade
            )

            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    f"✓ Класс изменён на {grade}.\n\n"
                    "Сохранённые олимпиады удалены.\n"
                    "Выбери олимпиады заново:"
                ),
                attachments=[
                    olympiad_selection_keyboard()
                ]
            )

            return

        # Обычная первичная настройка
        self.user_service.set_grade(
            user_id=user_id,
            grade=grade
        )

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                f"✓ Выбран {grade} класс.\n\n"
                "Теперь выбери интересующие тебя предметы:"
            ),
            attachments=[
                subjects_keyboard(set())
            ]
        )

    def handle_subject(self, user_id, message_id, payload):

        subject = payload.split(":")[1]

        self.user_service.toggle_subject(
            user_id=user_id,
            subject=subject
        )

        user = self.user_service.get_user(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                f"✓ Выбран {user.grade} класс.\n\n"
                "Выбери интересующие тебя предметы:"
            ),
            attachments=[
                subjects_keyboard(user.subjects)
            ]
        )

    def handle_subjects_done(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        if user.edit_mode == "subjects":

            if not user.subjects:
                self.max_client.edit_message(
                    message_id=message_id,
                    text="⚠ Выбери хотя бы один предмет.",
                    attachments=[
                        subjects_keyboard(user.subjects)
                    ]
                )
                return

            removed_subjects = self.user_service.finish_subjects_edit(
                user_id
            )

            print(
                f"Пользователь {user_id} удалил предметы: "
                f"{removed_subjects}"
            )

            # TODO: после подключения БД удалить
            # подписки на олимпиады по removed_subjects

            subject_names = [
                SUBJECTS[subject]
                for subject in user.subjects
            ]

            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    "✓ Предметы изменены.\n\n"
                    f"Предметы: {', '.join(subject_names)}"
                )
            )

            return

        if not user.subjects:
            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    f"✓ Выбран {user.grade} класс.\n\n"
                    "⚠ Выбери хотя бы один предмет."
                ),
                attachments=[subjects_keyboard(user.subjects)]
            )
            return

        subject_names = [
            SUBJECTS[subject]
            for subject in user.subjects
        ]

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                f"✓ Класс: {user.grade}\n"
                f"✓ Предметы: {', '.join(subject_names)}\n\n"
                "Как выбрать олимпиады?"
            ),
            attachments=[olympiad_selection_keyboard()]
        )

    def handle_levels_start(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text="Выбери уровни олимпиад:",
            attachments=[
                levels_keyboard(user.selected_levels)
            ]
        )


    def handle_level(self, user_id, message_id, payload):

        level = int(payload.split(":")[1])

        self.user_service.toggle_level(
            user_id=user_id,
            level=level
        )

        user = self.user_service.get_user(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text="Выбери уровни олимпиад:",
            attachments=[
                levels_keyboard(user.selected_levels)
            ]
        )


    def handle_levels_done(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        if not user.selected_levels:
            self.max_client.edit_message(
                message_id=message_id,
                text="⚠ Выбери хотя бы один уровень.",
                attachments=[
                    levels_keyboard(user.selected_levels)
                ]
            )
            return

        levels = ", ".join(
            str(level)
            for level in sorted(user.selected_levels)
        )

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                "✓ Настройка завершена!\n\n"
                f"Класс: {user.grade}\n"
                f"Уровни олимпиад: {levels}"
            )
        )


    def handle_all_olympiads(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                "✓ Настройка завершена!\n\n"
                f"Класс: {user.grade}\n"
                "Олимпиады: все подходящие.\n\n"
                "Когда подключим базу, здесь сформируется "
                "конкретный список олимпиад."
            )
        )


    def handle_specific_olympiads(self, message_id):

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                "Выбор конкретных олимпиад будет доступен "
                "после подключения базы данных."
            )
        )

    def handle_profile_grade(self, user_id, message_id):

        self.user_service.start_grade_edit(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text="Выбери новый класс:",
            attachments=[
                grade_keyboard()
            ]
        )

    def handle_profile_subjects(self, user_id, message_id):

        self.user_service.start_subjects_edit(user_id)

        user = self.user_service.get_user(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text="Измени список интересующих тебя предметов:",
            attachments=[
                subjects_keyboard(user.subjects)
            ]
        )

    def handle_profile_olympiads(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                f"Сохранено олимпиад: {len(user.olympiads)}.\n\n"
                "Список олимпиад подключим после появления базы данных."
            )
        )