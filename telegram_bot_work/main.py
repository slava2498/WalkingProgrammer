from telebot.async_telebot import AsyncTeleBot
import uvicorn
from ollama import chat

from telebot.types import Update as TelebotUpdate
from fastapi import FastAPI, Request

TOKEN = ''
bot = AsyncTeleBot(TOKEN)
app = FastAPI()


@bot.message_handler(content_types=['text'])
async def handler_start(message):
    print(message.chat)
    response_deepseek = chat(model='deepseek-r1:1.5b', messages=[
        {
            'role': 'user',
            'content': message.text
        },
    ])

    await bot.send_message(chat_id=message.chat.id, text=response_deepseek.message.content)


@app.post("/bot", status_code=200)
async def webhook(request: Request):
    # request_body_dict = await request.json()
    # update = TelebotUpdate.de_json(request_body_dict)
    # await bot.process_new_updates([update])
    return 'ok'


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)