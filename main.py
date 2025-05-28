from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import random
import string
import uvicorn
import os

DATABASE_URL = "postgresql://user:password@localhost/lol_stats_db"

DATABASE_URL = "sqlite:///./lol_stats.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String)
    password_hash = Column(String)
    race_class = Column(String)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    failed_attempts = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LoL Stats Service", description="Сервис игровой статистики для League of Legends")

templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_absurd_task():
    tasks = [
        "Решите: Сколько чемпионов в LoL умеют летать задом наперед?",
        "Введите количество пикселей в логотипе Riot Games:",
        "Сколько раз Ясуо умер в вашей последней игре? (если не играли, придумайте)",
        "Какой цвет получится, если смешать синий и красный в мире Рунтерры?",
        "Введите ваш любимый номер от 1 до 999999:",
    ]
    return random.choice(tasks)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, step: int = 1):
    absurd_task = generate_absurd_task()
    races = ["Эльф-программист", "Орк-аналитик", "Гном-тестировщик", "Человек-менеджер", "Дракон-DevOps"]

    return templates.TemplateResponse("register.html", {
        "request": request,
        "step": step,
        "absurd_task": absurd_task,
        "races": races,
        "random_number": random.randint(1, 100)
    })

@app.post("/register")
async def register_user(
        request: Request,
        username: str = Form(...),
        phone_number: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        race_class: str = Form(...),
        absurd_answer: str = Form(...),
        captcha_answer: str = Form(...),
        db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400,
                            detail="Пользователь уже существует! Попробуйте другое имя или страдайте дальше.")

    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Имя слишком короткое! В нашем мире имена должны быть длиннее.")

    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Пароли не совпадают! Это плохая примета.")

    if not phone_number.startswith("+7") or len(phone_number) != 12:
        raise HTTPException(status_code=400,
                            detail="Номер телефона должен начинаться с +7 и содержать ровно 12 символов!")

    if captcha_answer != "42":
        raise HTTPException(status_code=400, detail="Неверная капча! Правильный ответ всегда 42.")

    if random.random() < 0.3:
        raise HTTPException(status_code=400, detail="Сервер решил, что вы недостойны регистрации. Попробуйте еще раз.")

    hashed_password = get_password_hash(password)
    user = User(
        username=username,
        phone_number=phone_number,
        password_hash=hashed_password,
        race_class=race_class
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(url="/login?registered=true", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, registered: bool = False):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "registered": registered
    })

@app.post("/login")
async def login_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):

        if user:
            user.failed_attempts += 1
            db.commit()

        raise HTTPException(status_code=400,
                            detail="Неверные учетные данные! Или вы забыли пароль, или мы вас не помним.")

    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/stats")
async def get_stats():
    return {
        "message": "Функционал недоступен из-за технических работ или ваших собственных сомнений.",
        "error": "В нашем мире работающее ПО - плохая примета",
        "suggestion": "Попробуйте помедитировать или выпить чай"
    }

@app.get("/api/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "race_class": user.race_class,
            "registration_date": user.registration_date,
            "failed_attempts": user.failed_attempts
        }
        for user in users
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)