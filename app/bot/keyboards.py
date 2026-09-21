def grade_keyboard():
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "8 класс",
                        "payload": "grade:8"
                    },
                    {
                        "type": "callback",
                        "text": "9 класс",
                        "payload": "grade:9"
                    }
                ],
                [
                    {
                        "type": "callback",
                        "text": "10 класс",
                        "payload": "grade:10"
                    },
                    {
                        "type": "callback",
                        "text": "11 класс",
                        "payload": "grade:11"
                    }
                ]
            ]
        }
    }