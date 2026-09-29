from app.bot.keyboards import (
    subjects_keyboard,
    olympiad_selection_keyboard,
    levels_keyboard,
    grade_keyboard,
    my_olympiads_keyboard, profile_keyboard,
    specific_olympiads_keyboard,
    setup_complete_keyboard,
    deadlines_keyboard
)
from app.constants import SUBJECTS, AVAILABLE_SUBJECTS


class CallbackHandler:

    def __init__(
            self,
            max_client,
            user_service,
            olympiad_service
    ):
        self.max_client = max_client
        self.user_service = user_service
        self.olympiad_service = olympiad_service

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

        elif payload == "restart:confirm":
            self.handle_restart_confirm(
                user_id=user_id,
                message_id=message_id
            )

        elif payload == "restart:cancel":
            self.handle_restart_cancel(
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
                user_id=user_id,
                message_id=message_id
            )

        elif payload.startswith("specific:toggle:"):
            self.handle_specific_toggle(
                user_id=user_id,
                message_id=message_id,
                payload=payload
            )

        elif payload.startswith("specific:page:"):
            self.handle_specific_page(
                user_id=user_id,
                message_id=message_id,
                payload=payload
            )

        elif payload == "specific:done":
            self.handle_specific_done(
                user_id=user_id,
                message_id=message_id
            )

        elif payload.startswith("olympiad:remove:"):
            self.handle_remove_olympiad(
                user_id=user_id,
                message_id=message_id,
                payload=payload
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

        elif payload == "profile:deadlines":
            self.handle_profile_deadlines(
                user_id=user_id,
                message_id=message_id
            )

        elif payload.startswith("deadlines:page:"):
            self.handle_deadlines_page(
                user_id=user_id,
                message_id=message_id,
                payload=payload
            )

        elif payload == "profile:back":
            self.handle_profile_back(
                user_id=user_id,
                message_id=message_id
            )

        elif payload.startswith("olympiads:page:"):
            self.handle_olympiads_page(
                user_id=user_id,
                message_id=message_id,
                payload=payload
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

        subject_code = payload.split(":")[1]

        user = self.user_service.get_user(user_id)

        if subject_code not in AVAILABLE_SUBJECTS:
            subject_name = SUBJECTS.get(
                subject_code,
                "этому предмету",
            )

            selected_subjects = self.user_service.get_subjects(
                user_id
            )

            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    f"По предмету «{subject_name}» "
                    "пока нет олимпиад в базе.\n\n"
                    "Выбери другой предмет:"
                ),
                attachments=[
                    subjects_keyboard(selected_subjects)
                ]
            )

            return

        self.user_service.toggle_subject(
            user_id=user_id,
            subject_code=subject_code
        )

        selected_subjects = self.user_service.get_subjects(
            user_id
        )

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                f"✓ Выбран {user.grade} класс.\n\n"
                "Выбери интересующие тебя предметы:"
            ),
            attachments=[
                subjects_keyboard(selected_subjects)
            ]
        )

    def handle_subjects_done(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        selected_subjects = self.user_service.get_subjects(
            user_id
        )

        if not selected_subjects:
            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    f"✓ Выбран {user.grade} класс.\n\n"
                    "⚠ Выбери хотя бы один предмет."
                ),
                attachments=[
                    subjects_keyboard(selected_subjects)
                ]
            )
            return

        subject_names = [
            SUBJECTS[subject]
            for subject in selected_subjects
        ]

        # Если редактировали предметы из профиля
        if user.edit_mode == "subjects":
            self.user_service.remove_irrelevant_olympiads(
                user_id
            )

            self.user_service.finish_subjects_edit(
                user_id
            )

            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    "✓ Предметы изменены.\n\n"
                    f"Предметы: {', '.join(subject_names)}\n\n"
                    "Олимпиады по удалённым предметам "
                    "удалены из сохранённых."
                ),
                attachments=[
                    profile_keyboard()
                ]
            )

            return

        # Первичная настройка
        self.max_client.edit_message(
            message_id=message_id,
            text=(
                f"✓ Класс: {user.grade}\n"
                f"✓ Предметы: {', '.join(subject_names)}\n\n"
                "Как выбрать олимпиады?"
            ),
            attachments=[
                olympiad_selection_keyboard()
            ]
        )

    def handle_levels_start(self, user_id, message_id):

        selected_levels = self.user_service.get_selected_levels(
            user_id
        )

        self.max_client.edit_message(
            message_id=message_id,
            text="Выбери уровни олимпиад:",
            attachments=[
                levels_keyboard(selected_levels)
            ]
        )

    def handle_level(self, user_id, message_id, payload):

        level = int(payload.split(":")[1])

        self.user_service.toggle_level(
            user_id=user_id,
            level=level
        )

        selected_levels = self.user_service.get_selected_levels(
            user_id
        )

        self.max_client.edit_message(
            message_id=message_id,
            text="Выбери уровни олимпиад:",
            attachments=[
                levels_keyboard(selected_levels)
            ]
        )

    def handle_levels_done(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        selected_levels = self.user_service.get_selected_levels(
            user_id
        )

        selected_subjects = self.user_service.get_subjects(
            user_id
        )

        if not selected_levels:
            self.max_client.edit_message(
                message_id=message_id,
                text="⚠ Выбери хотя бы один уровень.",
                attachments=[
                    levels_keyboard(selected_levels)
                ]
            )
            return

        olympiads = self.olympiad_service.find_for_user(
            grade=user.grade,
            subject_codes=selected_subjects,
            levels=selected_levels
        )

        if not olympiads:
            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    "По выбранным предметам, классу "
                    "и уровням олимпиад ничего не найдено."
                )
            )
            return

        self.user_service.set_olympiads(
            user_id=user_id,
            olympiads=olympiads
        )

        olympiad_names = [
            f"• {olympiad.name} — {olympiad.level} уровень"
            for olympiad in olympiads
        ]

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                    "✓ Подходящие олимпиады:\n\n"
                    + "\n".join(olympiad_names)
            ),
            attachments=[
                setup_complete_keyboard()
            ]
        )

    def handle_all_olympiads(self, user_id, message_id):

        user = self.user_service.get_user(user_id)

        selected_subjects = self.user_service.get_subjects(
            user_id
        )

        olympiads = self.olympiad_service.find_for_user(
            grade=user.grade,
            subject_codes=selected_subjects
        )

        if not olympiads:
            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    "По выбранным настройкам "
                    "подходящих олимпиад не найдено."
                )
            )
            return

        self.user_service.set_olympiads(
            user_id=user_id,
            olympiads=olympiads
        )

        olympiad_names = [
            f"• {olympiad.name} — {olympiad.level} уровень"
            for olympiad in olympiads
        ]

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                    "✓ Подходящие олимпиады:\n\n"
                    + "\n".join(olympiad_names)
            ),
            attachments=[
                setup_complete_keyboard()
            ]
        )

    def handle_specific_olympiads(
            self,
            user_id,
            message_id,
            page=0
    ):
        user = self.user_service.get_user(user_id)

        selected_subjects = self.user_service.get_subjects(
            user_id
        )

        olympiads = self.olympiad_service.find_for_user(
            grade=user.grade,
            subject_codes=selected_subjects
        )

        if not olympiads:
            self.max_client.edit_message(
                message_id=message_id,
                text="Подходящих олимпиад не найдено."
            )
            return

        selected_ids = {
            str(olympiad.id)
            for olympiad in user.olympiads
        }

        self.max_client.edit_message(
            message_id=message_id,
            text="Выбери конкретные олимпиады:",
            attachments=[
                specific_olympiads_keyboard(
                    olympiads=olympiads,
                    selected_ids=selected_ids,
                    page=page,
                    page_size=5
                )
            ]
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

        selected_subjects = self.user_service.get_subjects(
            user_id
        )

        self.max_client.edit_message(
            message_id=message_id,
            text="Измени список интересующих тебя предметов:",
            attachments=[
                subjects_keyboard(selected_subjects)
            ]
        )

    def handle_profile_olympiads(
            self,
            user_id,
            message_id,
            page=0
    ):
        user = self.user_service.get_user(user_id)

        if not user.olympiads:
            self.max_client.edit_message(
                message_id=message_id,
                text="У тебя пока нет сохранённых олимпиад.",
                attachments=[
                    profile_keyboard()
                ]
            )
            return

        page_size = 5

        total_pages = max(
            1,
            (len(user.olympiads) + page_size - 1) // page_size
        )

        page = max(0, min(page, total_pages - 1))

        start = page * page_size
        end = start + page_size

        page_olympiads = user.olympiads[start:end]

        olympiad_names = []

        for olympiad in page_olympiads:
            subjects = ", ".join(
                subject.name
                for subject in olympiad.subjects
            )

            olympiad_names.append(
                f"• {olympiad.name}\n"
                f"  Предмет: {subjects}\n"
                f"  Уровень: {olympiad.level}"
            )

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                    "🏆 Мои олимпиады:\n\n"
                    + "\n".join(olympiad_names)
            ),
            attachments=[
                my_olympiads_keyboard(
                    user.olympiads,
                    page=page,
                    page_size=page_size
                )
            ]
        )

    def handle_olympiads_page(
            self,
            user_id,
            message_id,
            payload
    ):
        page = int(payload.split(":")[2])

        self.handle_profile_olympiads(
            user_id=user_id,
            message_id=message_id,
            page=page
        )

    def handle_profile_back(
            self,
            user_id,
            message_id
    ):
        user = self.user_service.get_user(user_id)

        subject_codes = self.user_service.get_subjects(user_id)

        subject_names = [
            SUBJECTS[code]
            for code in subject_codes
        ]

        subjects_text = ", ".join(subject_names)

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                "👤 Твой профиль\n\n"
                f"Класс: {user.grade}\n"
                f"Предметы: {subjects_text}"
            ),
            attachments=[
                profile_keyboard()
            ]
        )

    def handle_profile_deadlines(
            self,
            user_id,
            message_id,
            page=0,
    ):
        user = self.user_service.get_user(user_id)

        if not user.olympiads:
            self.max_client.edit_message(
                message_id=message_id,
                text="У тебя пока нет сохранённых олимпиад.",
                attachments=[
                    profile_keyboard()
                ]
            )
            return

        dated_events = []
        unknown_events = []

        for olympiad in user.olympiads:

            subjects_text = ", ".join(
                subject.name
                for subject in olympiad.subjects
            )

            for stage in olympiad.stages:

                # Точные даты
                events = [
                    (
                        stage.registration_start,
                        f"Начало регистрации — {stage.name}",
                    ),
                    (
                        stage.registration_end,
                        f"Конец регистрации — {stage.name}",
                    ),
                    (
                        stage.stage_start,
                        f"Начало этапа — {stage.name}",
                    ),
                    (
                        stage.stage_end,
                        f"Конец этапа — {stage.name}",
                    ),
                ]

                for event_date, event_name in events:

                    # None больше НЕ считается неизвестным сроком
                    if event_date is not None:
                        dated_events.append(
                            (
                                event_date,
                                olympiad.name,
                                subjects_text,
                                event_name,
                            )
                        )

                # raw_value нужен только тогда, когда
                # точную дату этапа определить не удалось.
                if (
                        stage.raw_value
                        and stage.stage_start is None
                        and stage.stage_end is None
                ):
                    unknown_events.append(
                        (
                            olympiad.name,
                            subjects_text,
                            stage.name,
                            stage.raw_value,
                        )
                    )

        # Сначала ближайшие события
        dated_events.sort(
            key=lambda item: item[0]
        )

        # Формируем готовые блоки.
        # Один элемент списка = одно событие.
        event_blocks = []

        for (
                event_date,
                olympiad_name,
                subjects_text,
                event_name,
        ) in dated_events:
            event_blocks.append(
                f"{event_date:%d.%m.%Y} — {olympiad_name}\n"
                f"📚 {subjects_text}\n"
                f"• {event_name}"
            )

        # Неопределённые сроки идут после всех точных
        for (
                olympiad_name,
                subjects_text,
                stage_name,
                raw_value,
        ) in unknown_events:
            event_blocks.append(
                f"❔ {olympiad_name}\n"
                f"📚 {subjects_text}\n"
                f"• {stage_name}: {raw_value}"
            )

        if not event_blocks:
            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    "📅 Для сохранённых олимпиад "
                    "пока нет известных сроков."
                ),
                attachments=[
                    profile_keyboard()
                ]
            )
            return

        # Не отправляем огромный текст одним сообщением.
        page_size = 6

        total_pages = max(
            1,
            (len(event_blocks) + page_size - 1) // page_size
        )

        page = max(
            0,
            min(page, total_pages - 1)
        )

        start = page * page_size
        end = start + page_size

        page_events = event_blocks[start:end]

        text = (
                "📅 Все сроки:\n\n"
                + "\n\n".join(page_events)
        )

        self.max_client.edit_message(
            message_id=message_id,
            text=text,
            attachments=[
                deadlines_keyboard(
                    page=page,
                    total_pages=total_pages,
                )
            ]
        )

    def handle_deadlines_page(
            self,
            user_id,
            message_id,
            payload,
    ):
        page = int(payload.split(":")[2])

        self.handle_profile_deadlines(
            user_id=user_id,
            message_id=message_id,
            page=page,
        )

    def handle_remove_olympiad(
            self,
            user_id,
            message_id,
            payload
    ):
        parts = payload.split(":")

        olympiad_id = parts[2]
        page = int(parts[3])

        self.user_service.remove_olympiad(
            user_id=user_id,
            olympiad_id=olympiad_id
        )

        self.handle_profile_olympiads(
            user_id=user_id,
            message_id=message_id,
            page=page
        )

    def handle_specific_toggle(
            self,
            user_id,
            message_id,
            payload
    ):
        parts = payload.split(":")

        olympiad_id = parts[2]
        page = int(parts[3])

        olympiad = self.olympiad_service.get_olympiad(
            olympiad_id
        )

        if olympiad is None:
            return

        self.user_service.toggle_olympiad(
            user_id=user_id,
            olympiad=olympiad
        )

        self.handle_specific_olympiads(
            user_id=user_id,
            message_id=message_id,
            page=page
        )

    def handle_specific_page(
            self,
            user_id,
            message_id,
            payload
    ):
        page = int(payload.split(":")[2])

        self.handle_specific_olympiads(
            user_id=user_id,
            message_id=message_id,
            page=page
        )

    def handle_specific_done(
            self,
            user_id,
            message_id
    ):
        user = self.user_service.get_user(user_id)

        if not user.olympiads:
            self.max_client.edit_message(
                message_id=message_id,
                text=(
                    "Выбери хотя бы одну олимпиаду."
                )
            )
            return

        olympiad_names = [
            f"• {olympiad.name} — {olympiad.level} уровень"
            for olympiad in user.olympiads
        ]

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                    "✓ Олимпиады сохранены:\n\n"
                    + "\n".join(olympiad_names)
            ),
            attachments=[
                setup_complete_keyboard()
            ]
        )

    def handle_restart_confirm(
            self,
            user_id,
            message_id
    ):
        self.user_service.reset_user(user_id)

        self.max_client.edit_message(
            message_id=message_id,
            text=(
                "Профиль очищен.\n\n"
                "В каком классе ты учишься?"
            ),
            attachments=[
                grade_keyboard()
            ]
        )

    def handle_restart_cancel(
            self,
            message_id
    ):
        self.max_client.edit_message(
            message_id=message_id,
            text="Настройка отменена. Данные профиля сохранены."
        )