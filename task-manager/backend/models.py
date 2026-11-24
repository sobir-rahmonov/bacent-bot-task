from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    first_name = Column(String(100))
    username = Column(String(100))

    tasks = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship(
        "User",
        back_populates="tasks"
    )