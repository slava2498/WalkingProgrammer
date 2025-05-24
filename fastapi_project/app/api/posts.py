from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from fastapi_project.app.database.database import engine
from fastapi_project.models import Post

router = APIRouter(prefix='/posts', tags=['posts'])

BASE_URL = 'https://jsonplaceholder.typicode.com/posts'


class PostModel(BaseModel):
    id: int
    title: str
    body: str
    user_id: int


class PostCreateModel(BaseModel):
    title: str
    body: str
    user_id: int


@router.get("/", status_code=200)
async def get_posts() -> List[PostModel]:
    async with engine.connect() as conn:
        result = await conn.execute(select(Post).select_from(Post))
        return [
            PostModel(
                id=data.id,
                title=data.title,
                body=data.body,
                user_id=data.user_id
            )
            for data in result.all()
        ]


@router.get("/{post_id}", status_code=200)
async def get_post(post_id: int) -> PostModel:
    async with engine.connect() as conn:
        result = await conn.execute(select(Post).select_from(Post).where(Post.id == post_id))
        data = result.first()
        return PostModel(
            id=data.id,
            title=data.title,
            body=data.body,
            user_id=data.user_id
        )


@router.post("/", status_code=201)
async def create_post(post: PostCreateModel):
    async with engine.connect() as conn:
        await conn.execute(insert(Post).values({
            Post.title: post.title,
            Post.body: post.body,
            Post.user_id: post.user_id,
        }))
        await conn.commit()


@router.put("/{post_id}", status_code=204)
async def update_post(post_id: int, post: PostCreateModel):
    async with engine.connect() as conn:
        await conn.execute(update(Post).values({
            Post.title: post.title,
            Post.body: post.body,
            Post.user_id: post.user_id,
        }).where(Post.id == post_id))
        await conn.commit()


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int):
    async with engine.connect() as conn:
        await conn.execute(delete(Post).where(Post.id == post_id))
        await conn.commit()
