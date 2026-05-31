LIMITS = {
    'project_title': 200,
    'skill_title': 124,
    'user_name': 124,
    'user_surname': 124,
    'user_phone': 12,
    'user_bio': 256,
    'status_field': 6,
    'min_password': 8,
    'per_page': 12,
    'autocomplete': 10,
    'avatar_size': 200,
    'avatar_font': 120,
}

STATE = {
    'active': 'open',
    'done': 'closed',
}

STATE_OPTIONS = [
    (STATE['active'], 'Открыт'),
    (STATE['done'], 'Закрыт'),
]

PALETTE = {
    'backgrounds': [
        (66, 133, 243), (219, 68, 55), (244, 180, 0),
        (15, 157, 88), (171, 71, 189), (0, 172, 193),
        (255, 112, 67),
    ],
    'foreground': 'white',
    'image_type': 'PNG',
    'origin': (0, 0),
}

MESSAGES = {
    'access_denied': 'Только автор может выполнить это действие',
    'already_finished': 'Проект уже завершён',
    'project_missing': 'Проект не найден',
    'user_missing': 'Пользователь не найден',
    'skill_missing': 'Навык не найден',
    'not_your_profile': 'Нельзя редактировать чужой профиль',
    'bad_json': 'Неверный формат данных',
    'skill_data_required': 'Нужно передать skill_id или title',
    'skill_not_present': 'Этого навыка нет',
    'auth_failed': 'Неверный email или пароль',
    'phone_invalid': 'Формат: +7XXXXXXXXXX или 8XXXXXXXXXX',
    'phone_short': 'Номер должен содержать 11 цифр',
    'phone_nan': 'Номер должен содержать только цифры',
    'phone_taken': 'Этот номер уже используется',
    'email_taken': 'Этот email уже зарегистрирован',
    'github_bad': 'Ссылка должна вести на Github',
    'wrong_password': 'Неверный старый пароль',
    'password_mismatch': 'Новые пароли не совпадают',
}
