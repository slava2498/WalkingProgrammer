import uvicorn

from fastapi import FastAPI

from api import posts, comments, albums, photos, todos, users

app = FastAPI()


app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(albums.router)
app.include_router(photos.router)
app.include_router(todos.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to our FastAPI!"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)