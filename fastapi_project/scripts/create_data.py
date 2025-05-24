import asyncio
import json
import random

from sqlalchemy import insert, select

from fastapi_project.app.database.database import engine
from fastapi_project.models import Post, Comment, Album, Photo, Todo, User


def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


async def create(table, data):
    async with engine.connect() as conn:
        await conn.execute(insert(table), data)
        await conn.commit()


async def main():
    posts_data = load_data("posts.json")
    comments_data = load_data("comments.json")
    albums_data = load_data("albums.json")
    photos_data = load_data("photos.json")
    todos_data = load_data("todos.json")
    users_data = load_data("users.json")

    users_data = [{
        key: value
        for key, value in data.items()
        if key not in {'address', 'phone', 'website', 'company'}
    } for data in users_data]

    comments_data = [{
        key: value
        for key, value in data.items()
        if key not in {'email', 'name'}
    } for data in comments_data]

    photos_data = [{
        key: value
        for key, value in data.items()
        if key not in {'thumbnailUrl'}
    } for data in photos_data]

    await create(User, users_data)

    async with engine.connect() as conn:
        users = await conn.execute(select(User.id).select_from(User))
        users_ids = [user.id for user in users]

    for data in comments_data:
        data['user_id'] = random.choice(users_ids)

    for data in photos_data:
        data['album_id'] = data['albumId']
        data.pop('albumId')

    await create(Post, posts_data)
    await create(Comment, comments_data)
    await create(Album, albums_data)
    await create(Photo, photos_data)
    await create(Todo, todos_data)


if __name__ == '__main__':
    asyncio.run(main())