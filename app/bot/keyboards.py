from app.constants import GRADES, SUBJECTS, OLYMPIAD_LEVELS


def grade_keyboard():
    buttons = []

    for i in range(0, len(GRADES), 2):
        row = []

        for grade in GRADES[i:i + 2]:
            row.append({
                "type": "callback",
                "text": f"{grade} класс",
                "payload": f"grade:{grade}"
            })

        buttons.append(row)

    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": buttons }
    }


def subjects_keyboard(selected_subjects: set[str]):

    s_buttons = []

    for code, name in SUBJECTS.items():

        if code in selected_subjects:
            text = f"✓ {name}"
        else:
            text = name

        s_buttons.append({
            "type": "callback",
            "text": text,
            "payload": f"subject:{code}"
        })

    buttons = []

    for i in range(0, len(s_buttons), 2):
        buttons.append(s_buttons[i:i + 2])

    # Отдельная кнопка "Готово"
    buttons.append([
        {
            "type": "callback",
            "text": "Готово",
            "payload": "subjects:done"
        }
    ])

    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": buttons
        }
    }

def olympiad_selection_keyboard():
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "Все подходящие",
                        "payload": "olympiads:all"
                    }
                ],
                [
                    {
                        "type": "callback",
                        "text": "По уровню",
                        "payload": "olympiads:levels"
                    }
                ],
                [
                    {
                        "type": "callback",
                        "text": "Выбрать конкретные",
                        "payload": "olympiads:specific"
                    }
                ]
            ]
        }
    }


def levels_keyboard(selected_levels: set[int]):
    buttons = []

    for level, name in OLYMPIAD_LEVELS.items():

        text = f"✓ {name}" if level in selected_levels else name

        buttons.append([
            {
                "type": "callback",
                "text": text,
                "payload": f"level:{level}"
            }
        ])

    buttons.append([
        {
            "type": "callback",
            "text": "Готово",
            "payload": "levels:done"
        }
    ])

    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": buttons
        }
    }

def profile_keyboard():
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "Изменить класс",
                        "payload": "profile:grade"
                    }
                ],
                [
                    {
                        "type": "callback",
                        "text": "Изменить предметы",
                        "payload": "profile:subjects"
                    }
                ],
                [
                    {
                        "type": "callback",
                        "text": "Мои олимпиады",
                        "payload": "profile:olympiads"
                    }
                ]
            ]
        }
    }

def my_olympiads_keyboard(
    olympiads,
    page: int = 0,
    page_size: int = 5
):
    buttons = []

    total = len(olympiads)
    total_pages = max(1, (total + page_size - 1) // page_size)

    # Чтобы страница не вышла за допустимые границы
    page = max(0, min(page, total_pages - 1))

    start = page * page_size
    end = start + page_size

    page_olympiads = olympiads[start:end]

    # Олимпиады текущей страницы
    for olympiad in page_olympiads:
        buttons.append([
            {
                "type": "callback",
                "text": f"❌ {olympiad.name}",
                "payload": f"olympiad:remove:{olympiad.id}:{page}"
            }
        ])

    # Перелистывание
    if total_pages > 1:
        navigation = []

        if page > 0:
            navigation.append({
                "type": "callback",
                "text": "◀️",
                "payload": f"olympiads:page:{page - 1}"
            })

        navigation.append({
            "type": "callback",
            "text": f"{page + 1} / {total_pages}",
            "payload": "olympiads:page_info"
        })

        if page < total_pages - 1:
            navigation.append({
                "type": "callback",
                "text": "▶️",
                "payload": f"olympiads:page:{page + 1}"
            })

        buttons.append(navigation)

    # Назад в профиль
    buttons.append([
        {
            "type": "callback",
            "text": "← Назад",
            "payload": "profile:back"
        }
    ])

    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": buttons
        }
    }

def specific_olympiads_keyboard(
    olympiads,
    selected_ids: set[str],
    page: int = 0,
    page_size: int = 5
):
    buttons = []

    total = len(olympiads)
    total_pages = max(1, (total + page_size - 1) // page_size)

    page = max(0, min(page, total_pages - 1))

    start = page * page_size
    end = start + page_size

    page_olympiads = olympiads[start:end]

    for olympiad in page_olympiads:

        olympiad_id = str(olympiad.id)

        if olympiad_id in selected_ids:
            text = f"✓ {olympiad.name}"
        else:
            text = olympiad.name

        buttons.append([
            {
                "type": "callback",
                "text": text,
                "payload": (
                    f"specific:toggle:{olympiad.id}:{page}"
                )
            }
        ])

    if total_pages > 1:
        navigation = []

        if page > 0:
            navigation.append({
                "type": "callback",
                "text": "◀️",
                "payload": f"specific:page:{page - 1}"
            })

        navigation.append({
            "type": "callback",
            "text": f"{page + 1} / {total_pages}",
            "payload": "specific:page_info"
        })

        if page < total_pages - 1:
            navigation.append({
                "type": "callback",
                "text": "▶️",
                "payload": f"specific:page:{page + 1}"
            })

        buttons.append(navigation)

    buttons.append([
        {
            "type": "callback",
            "text": "Готово",
            "payload": "specific:done"
        }
    ])

    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": buttons
        }
    }

def restart_keyboard():
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "⚠️ Начать заново",
                        "payload": "restart:confirm"
                    }
                ],
                [
                    {
                        "type": "callback",
                        "text": "Отмена",
                        "payload": "restart:cancel"
                    }
                ]
            ]
        }
    }