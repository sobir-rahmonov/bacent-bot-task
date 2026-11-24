from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    telegram_id: int
    first_name: str
    username: str | None = None


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    first_name: str
    username: str | None

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)