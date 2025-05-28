from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lol_stats.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """Модель пользователя для хранения данных регистрации"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    phone_number = Column(String(15), nullable=False)
    password_hash = Column(String(255), nullable=False)
    race_class = Column(String(100), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    failed_attempts = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', race_class='{self.race_class}')>"

class RegistrationAttempt(Base):
    """Модель для отслеживания попыток регистрации"""
    __tablename__ = "registration_attempts"

    id = Column(Integer, primary_key=True, index=True)
    username_attempt = Column(String(50), nullable=False)
    phone_attempt = Column(String(15), nullable=False)
    ip_address = Column(String(45), nullable=True)
    attempt_date = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)

class SystemLog(Base):
    """Модель для логирования системных событий"""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)

def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Зависимость для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_username(db, username: str):
    """Получить пользователя по имени"""
    return db.query(User).filter(User.username == username).first()

def create_user(db, user_data: dict):
    """Создать нового пользователя"""
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def log_registration_attempt(db, attempt_data: dict):
    """Записать попытку регистрации"""
    attempt = RegistrationAttempt(**attempt_data)
    db.add(attempt)
    db.commit()
    return attempt

def log_system_event(db, event_data: dict):
    """Записать системное событие"""
    log = SystemLog(**event_data)
    db.add(log)
    db.commit()
    return log

if __name__ == "__main__":

    create_tables()
    print("База данных инициализирована!")

    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    db = SessionLocal()
    try:
        test_user = get_user_by_username(db, "test_user")
        if not test_user:
            test_user_data = {
                "username": "test_user",
                "phone_number": "+71234567890",
                "password_hash": pwd_context.hash("test_password"),
                "race_class": "Эльф-программист"
            }
            create_user(db, test_user_data)
            print("Создан тестовый пользователь: test_user / test_password")
    finally:
        db.close()