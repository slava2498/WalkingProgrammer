from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from fastapi_project.app.database.database import engine
from fastapi_project.models import User

router = APIRouter(prefix='/users', tags=['users'])

BASE_URL = 'https://jsonplaceholder.typicode.com/users'


class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: str


@router.get("/", status_code=200)
async def get_users() -> List[UserModel]:
    async with engine.connect() as conn:
        result = await conn.execute(select(User).select_from(User))
        return [
            UserModel(
                id=data.id,
                name=data.name,
                username=data.username,
                email=data.email
            )
            for data in result.all()
        ]


@router.get("/{user_id}", status_code=200)
async def get_user(user_id: int) -> UserModel:
    async with engine.connect() as conn:
        result = await conn.execute(select(User).select_from(User).where(User.id == user_id))
        data = result.first()
        return UserModel(
            id=data.id,
            name=data.name,
            username=data.username,
            email=data.email
        )
