from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from fastapi_project.app.database.database import engine
from fastapi_project.models import Photo

router = APIRouter(prefix='/photos', tags=['photos'])

BASE_URL = 'https://jsonplaceholder.typicode.com/photos'


class PhotoModel(BaseModel):
    id: int
    title: str
    url: str
    album_id: int


@router.get("/", status_code=200)
async def get_photos() -> List[PhotoModel]:
    async with engine.connect() as conn:
        result = await conn.execute(select(Photo).select_from(Photo))
        return [
            PhotoModel(
                id=data.id,
                title=data.title,
                url=data.url,
                album_id=data.album_id,
            )
            for data in result.all()
        ]


@router.get("/{photo_id}", status_code=200)
async def get_post(photo_id: int):
    async with engine.connect() as conn:
        result = await conn.execute(select(Photo).select_from(Photo).where(Photo.id == photo_id))
        data = result.first()
        return PhotoModel(
            id=data.id,
            title=data.title,
            url=data.url,
            album_id=data.album_id,
        )