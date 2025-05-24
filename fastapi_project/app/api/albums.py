from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from fastapi_project.app.database.database import engine
from fastapi_project.models import Album

router = APIRouter(prefix='/albums', tags=['comments'])

BASE_URL = 'https://jsonplaceholder.typicode.com/albums'


class AlbumModel(BaseModel):
    id: int
    title: str
    user_id: int


@router.get("/", status_code=200)
async def get_albums() -> List[AlbumModel]:
    async with engine.connect() as conn:
        result = await conn.execute(select(Album).select_from(Album))
        return [
            AlbumModel(
                id=data.id,
                title=data.title,
                user_id=data.user_id,
            )
            for data in result.all()
        ]


@router.get("/{album_id}", status_code=200)
async def get_post(album_id: int):
    async with engine.connect() as conn:
        result = await conn.execute(select(Album).select_from(Album).where(Album.id == album_id))
        data = result.first()
        return AlbumModel(
            id=data.id,
            title=data.title,
            user_id=data.user_id,
        )