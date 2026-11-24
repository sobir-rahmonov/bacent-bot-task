from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User, Task
from schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/api",
    tags=["Tasks"]
)


@router.post(
    "/users/{user_id}/tasks",
    response_model=TaskResponse
)
def create_task(
    user_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(404, "User not found")

    task = Task(
        title=data.title,
        user_id=user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get(
    "/users/{user_id}/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    user_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Task).filter(
        Task.user_id == user_id
    ).all()


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}