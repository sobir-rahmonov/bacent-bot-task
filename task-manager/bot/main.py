
from contextlib import asynccontextmanager
from secrets import compare_digest

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from aiogram.types import Update

from database import engine, Base
import models

from routers import users, tasks
from bot import bot, dp
from backend.config import WEBHOOK_URL, WEBHOOK_SECRET


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Database jadvallari
    Base.metadata.create_all(bind=engine)

    # Telegram webhook o'rnatish
    await bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=dp.resolve_used_update_types()
    )

    print("Telegram Webhook registered!")
    print(f"Webhook URL: {WEBHOOK_URL}")

    yield

    # Server yopilganda bot sessiyasini yopish
    await bot.session.close()


app = FastAPI(
    title="Telegram Task Manager API",
    version="1.0.0",
    lifespan=lifespan
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# API routers
app.include_router(users.router)
app.include_router(tasks.router)


# Main endpoint
@app.get("/")
async def home():
    return {
        "status": "success",
        "message": "Telegram Task Manager API"
    }


# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}


# Telegram Webhook endpoint
@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):

    # Telegram maxfiy tokenini tekshirish
    received_secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token", ""
    )

    if not compare_digest(
        received_secret,
        WEBHOOK_SECRET
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook secret"
        )

    # Telegram update
    data = await request.json()

    update = Update.model_validate(
        data,
        context={"bot": bot}
    )

    # Aiogram dispatcher orqali qayta ishlash
    await dp.feed_update(bot, update)

    return {"ok": True}
