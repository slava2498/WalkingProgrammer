from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from fastapi_project.app.database.database import engine
from fastapi_project.models import Todo

router = APIRouter(prefix='/todos', tags=['todos'])

BASE_URL = 'https://jsonplaceholder.typicode.com/todos'


class TodoModel(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int


@router.get("/", status_code=200)
async def get_todos() -> List[TodoModel]:
    async with engine.connect() as conn:
        result = await conn.execute(select(Todo).select_from(Todo))
        return [
            TodoModel(
                id=data.id,
                title=data.title,
                completed=data.completed,
                user_id=data.user_id
            )
            for data in result.all()
        ]


@router.get("/{todo_id}", status_code=200)
async def get_post(todo_id: int):
    async with engine.connect() as conn:
        result = await conn.execute(select(Todo).select_from(Todo).where(Todo.id == todo_id))
        data = result.first()
        return TodoModel(
            id=data.id,
            title=data.title,
            completed=data.completed,
            user_id=data.user_id
        )