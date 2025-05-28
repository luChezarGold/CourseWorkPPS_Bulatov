"""
Конфигурационный файл для LoL Stats Service
"""

import os
from typing import Optional

class Settings:
    """Настройки приложения"""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./lol_stats.db"
    )

    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REGISTRATION_TIME_LIMIT_MINUTES: int = 15
    MAX_FAILED_ATTEMPTS: int = 5

    APP_NAME: str = "LoL Stats Service"
    APP_VERSION: str = "2025.1"
    APP_DESCRIPTION: str = "Сервис игровой статистики для League of Legends"

    ENABLE_ABSURD_REGISTRATION: bool = True
    ENABLE_BROKEN_FUNCTIONALITY: bool = True
    RANDOM_ERROR_PROBABILITY: float = 0.3

    REGISTRATION_SUCCESS_MESSAGE: str = (
        "Поздравляем! Вы успешно прошли испытание регистрации! "
        "Теперь вы можете насладиться неработоспособным функционалом."
    )

    BROKEN_FUNCTIONALITY_MESSAGE: str = (
        "Функционал недоступен из-за технических работ или ваших собственных сомнений."
    )

    TIMEOUT_MESSAGE: str = (
        "Время вышло! Вы не достойны быть частью этого мира."
    )

    AVAILABLE_RACES: list = [
        "Эльф-программист",
        "Орк-аналитик",
        "Гном-тестировщик",
        "Человек-менеджер",
        "Дракон-DevOps",
        "Хоббит-дизайнер",
        "Тролль-администратор"
    ]

    ABSURD_TASKS: list = [
        "Решите: Сколько чемпионов в LoL умеют летать задом наперед?",
        "Введите количество пикселей в логотипе Riot Games:",
        "Сколько раз Ясуо умер в вашей последней игре? (если не играли, придумайте)",
        "Какой цвет получится, если смешать синий и красный в мире Рунтерры?",
        "Введите ваш любимый номер от 1 до 999999:",
        "Сколько багов в среднем содержит одна строка кода?",
        "Назовите точное время, когда вы в последний раз выиграли в LoL:"
    ]

settings = Settings()

def get_database_url() -> str:
    """Получить URL базы данных"""
    return settings.DATABASE_URL

def is_debug_mode() -> bool:
    """Проверить, включен ли режим отладки"""
    return settings.DEBUG

def get_registration_time_limit() -> int:
    """Получить лимит времени на регистрацию в минутах"""
    return settings.REGISTRATION_TIME_LIMIT_MINUTES

def should_enable_absurd_features() -> bool:
    """Проверить, нужно ли включать абсурдные функции"""
    return settings.ENABLE_ABSURD_REGISTRATION

def get_random_race() -> str:
    """Получить случайную расу из списка"""
    import random
    return random.choice(settings.AVAILABLE_RACES)

def get_random_absurd_task() -> str:
    """Получить случайное абсурдное задание"""
    import random
    return random.choice(settings.ABSURD_TASKS)