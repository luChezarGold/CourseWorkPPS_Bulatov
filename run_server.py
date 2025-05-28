"""
Скрипт для запуска сервера LoL Stats Service
"""

import uvicorn
import os
import sys
from database import create_tables

def main():
    """Основная функция для запуска сервера"""

    print("🎮 Запуск LoL Stats Service...")
    print("=" * 50)

    try:
        create_tables()
        print("✅ База данных инициализирована")
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        sys.exit(1)

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    print(f"🌐 Сервер будет доступен по адресу: http://{host}:{port}")
    print(f"🔧 Режим отладки: {'Включен' if debug else 'Выключен'}")
    print("=" * 50)
    print("📋 Доступные страницы:")
    print(f"   • Главная: http://{host}:{port}/")
    print(f"   • Регистрация: http://{host}:{port}/register")
    print(f"   • Вход: http://{host}:{port}/login")
    print(f"   • Панель: http://{host}:{port}/dashboard")
    print(f"   • API документация: http://{host}:{port}/docs")
    print("=" * 50)
    print("⚠️  ВНИМАНИЕ: Это приложение создано для демонстрации")
    print("   абсурдной регистрации и неработоспособного функционала!")
    print("=" * 50)

    try:

        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=debug,
            log_level="info" if debug else "warning"
        )
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()