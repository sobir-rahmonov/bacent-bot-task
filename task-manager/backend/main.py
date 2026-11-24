from fastapi import FastAPI

from database import engine, Base
import models

from routers import users, tasks

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Telegram Task Manager API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Task Manager API is running"
    }
