from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db, User, RegistrationAttempt, SystemLog, log_system_event
from typing import List, Dict, Any
import random
from datetime import datetime, timedelta

api_router = APIRouter(prefix="/api", tags=["API"])


@api_router.get("/stats")
async def get_fake_stats():
    """
    Получение 'статистики' - неработоспособный функционал
    """
    fake_responses = [
        {
            "message": "Функционал недоступен из-за технических работ или ваших собственных сомнений.",
            "error": "В нашем мире работающее ПО - плохая примета",
            "suggestion": "Попробуйте помедитировать или выпить чай",
            "status": "broken_by_design"
        },
        {
            "message": "Статистика временно эмигрировала в параллельную вселенную",
            "error": "404: Данные не найдены в этой реальности",
            "suggestion": "Попробуйте поискать в другом измерении",
            "status": "interdimensional_error"
        },
        {
            "message": "Сервер решил взять отпуск",
            "error": "500: Внутренняя ошибка сервера (он устал)",
            "suggestion": "Дайте серверу отдохнуть",
            "status": "server_on_vacation"
        }
    ]

    return random.choice(fake_responses)


@api_router.get("/users", response_model=List[Dict[str, Any]])
async def get_users(db: Session = Depends(get_db)):
    """
    Получение списка зарегистрированных пользователей
    """
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "race_class": user.race_class,
            "registration_date": user.registration_date.isoformat(),
            "failed_attempts": user.failed_attempts,
            "is_active": user.is_active,
            "last_login": user.last_login.isoformat() if user.last_login else None
        }
        for user in users
    ]


@api_router.get("/registration-attempts")
async def get_registration_attempts(db: Session = Depends(get_db)):
    """
    Получение статистики попыток регистрации
    """
    attempts = db.query(RegistrationAttempt).order_by(RegistrationAttempt.attempt_date.desc()).limit(50).all()

    return {
        "total_attempts": len(attempts),
        "successful_attempts": len([a for a in attempts if a.success]),
        "failed_attempts": len([a for a in attempts if not a.success]),
        "recent_attempts": [
            {
                "username_attempt": attempt.username_attempt,
                "phone_attempt": attempt.phone_attempt,
                "attempt_date": attempt.attempt_date.isoformat(),
                "success": attempt.success,
                "error_message": attempt.error_message
            }
            for attempt in attempts[:10]
        ]
    }


@api_router.get("/system-logs")
async def get_system_logs(db: Session = Depends(get_db)):
    """
    Получение системных логов
    """
    logs = db.query(SystemLog).order_by(SystemLog.timestamp.desc()).limit(100).all()

    return [
        {
            "id": log.id,
            "event_type": log.event_type,
            "user_id": log.user_id,
            "description": log.description,
            "timestamp": log.timestamp.isoformat(),
            "ip_address": log.ip_address
        }
        for log in logs
    ]


@api_router.get("/fake-champion-stats")
async def get_fake_champion_stats():
    """
    Фейковая статистика чемпионов
    """
    champions = [
        "Yasuo", "Zed", "Lee Sin", "Thresh", "Jinx", "Ahri", "Garen", "Darius",
        "Katarina", "Riven", "Vayne", "Lucian", "Ezreal", "Lux", "Morgana"
    ]

    fake_stats = []
    for champion in random.sample(champions, 5):
        fake_stats.append({
            "champion": champion,
            "win_rate": f"{random.randint(30, 70)}%",
            "pick_rate": f"{random.randint(5, 25)}%",
            "ban_rate": f"{random.randint(0, 50)}%",
            "average_kda": f"{random.randint(1, 5)}.{random.randint(0, 9)}/{random.randint(3, 8)}.{random.randint(0, 9)}/{random.randint(5, 15)}.{random.randint(0, 9)}",
            "note": "Данные сгенерированы случайно и не отражают реальную статистику"
        })

    return {
        "message": "Внимание! Эта статистика полностью выдумана",
        "disclaimer": "В нашем мире точные данные - плохая примета",
        "champions": fake_stats,
        "last_updated": "Никогда",
        "reliability": "0%"
    }


@api_router.post("/submit-feedback")
async def submit_feedback(
        feedback: str,
        rating: int,
        request: Request,
        db: Session = Depends(get_db)
):
    """
    Отправка отзыва (который никуда не сохраняется)
    """
    # Логируем "отзыв"
    log_system_event(db, {
        "event_type": "feedback",
        "description": f"Получен отзыв: '{feedback}' с рейтингом {rating}",
        "ip_address": request.client.host
    })

    responses = [
        "Спасибо за отзыв! Мы его обязательно проигнорируем.",
        "Ваш отзыв очень важен для нас. Поэтому мы его удалили.",
        "Отзыв принят и отправлен в параллельную вселенную на рассмотрение.",
        "Благодарим за обратную связь! Она поможет нам стать еще хуже.",
        "Ваш отзыв сохранен в нашей базе данных несуществующих отзывов."
    ]

    return {
        "message": random.choice(responses),
        "feedback_id": f"FB-{random.randint(10000, 99999)}",
        "status": "ignored_successfully"
    }


@api_router.get("/server-status")
async def get_server_status():
    """
    Статус сервера (всегда проблемный)
    """
    statuses = [
        {
            "status": "Работает неправильно",
            "uptime": "5 минут (рекорд!)",
            "errors": random.randint(100, 999),
            "warnings": random.randint(50, 200),
            "memory_usage": f"{random.randint(80, 99)}%",
            "cpu_usage": f"{random.randint(70, 100)}%",
            "message": "Все идет по плану. План - сломать все."
        },
        {
            "status": "Критическая ошибка",
            "uptime": "Отрицательное время",
            "errors": "Слишком много для подсчета",
            "warnings": "Игнорируются",
            "memory_usage": "Вся доступная + немного чужой",
            "cpu_usage": "Больше 100% (не спрашивайте как)",
            "message": "Сервер работает на чистом энтузиазме и кофеине."
        }
    ]

    return random.choice(statuses)


@api_router.get("/random-quote")
async def get_random_quote():
    """
    Случайная 'мудрая' цитата
    """
    quotes = [
        "В мире программирования единственная константа - это баги.",
        "Код, который работает с первого раза, подозрителен.",
        "Лучший способ найти баг - показать код заказчику.",
        "Если программа работает, значит, вы что-то делаете не так.",
        "Документация - это теория. Код - это практика. Баги - это реальность.",
        "Программист - это человек, который решает проблемы, о существовании которых вы не подозревали, способами, которые вы не понимаете.",
        "Работающий код - это миф, как единороги и честные политики."
    ]

    return {
        "quote": random.choice(quotes),
        "author": "Неизвестный мудрец из IT",
        "category": "Программистская мудрость",
        "reliability": "Сомнительная"
    }