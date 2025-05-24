from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from fastapi_project.app.database.database import engine
from fastapi_project.models import Comment

router = APIRouter(prefix='/comments', tags=['comments'])

BASE_URL = 'https://jsonplaceholder.typicode.com/comments'


class CommentModel(BaseModel):
    id: int
    post_id: int
    user_id: int
    body: str


@router.get("/", status_code=200)
async def get_comments() -> List[CommentModel]:
    async with engine.connect() as conn:
        result = await conn.execute(select(Comment).select_from(Comment))
        return [
            CommentModel(
                id=data.id,
                post_id=data.post_id,
                user_id=data.user_id,
                body=data.body
            )
            for data in result.all()
        ]


@router.get("/{comment_id}", status_code=200)
async def get_post(comment_id: int) -> CommentModel:
    async with engine.connect() as conn:
        result = await conn.execute(select(Comment).select_from(Comment).where(Comment.id == comment_id))
        data = result.first()
        return CommentModel(
            id=data.id,
            post_id=data.post_id,
            user_id=data.user_id,
            body=data.body
        )