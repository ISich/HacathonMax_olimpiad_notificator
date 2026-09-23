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