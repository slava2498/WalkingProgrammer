import asyncio
import redis
import requests
from telebot.async_telebot import AsyncTeleBot

from config import TOKEN as DEEPSEEK_TOKEN, TELEGRAM_TOKEN

bot = AsyncTeleBot(TELEGRAM_TOKEN)


cache = redis.Redis(host="localhost", port=6379, db=0)
history_cache = {}

FAQ_CONTEXT = [
    {"role": "system", "content": "Ты – ассистент SkyFly Airlines. Отвечай коротко и точно."},

    # Документы для перелета
    {"role": "user", "content": "Какие документы нужны для внутреннего рейса?"},
    {"role": "assistant",
     "content": "Для внутренних рейсов SkyFly Airlines требуется паспорт РФ или водительское удостоверение."},
    {"role": "user", "content": "Какие документы нужны для международного рейса?"},
    {"role": "assistant",
     "content": "Для международных рейсов необходим загранпаспорт и, если требуется, виза в страну назначения."},
    {"role": "user", "content": "Нужна ли виза для поездки в США?"},
    {"role": "assistant",
     "content": "Да, для поездки в США необходимо оформить визу B1/B2 или получить разрешение ESTA."},

    # Багаж и ручная кладь
    {"role": "user", "content": "Сколько багажа можно взять бесплатно?"},
    {"role": "assistant",
     "content": "В SkyFly Airlines разрешено 1 место багажа до 23 кг бесплатно в тарифах 'Стандарт' и 'Премиум'."},
    {"role": "user", "content": "Можно ли провозить спортивный инвентарь?"},
    {"role": "assistant",
     "content": "Да, но необходимо оформить его как дополнительный багаж. Велосипеды, лыжи и доски — с доплатой."},

    # Перевозка животных
    {"role": "user", "content": "Можно ли перевозить животных в самолете?"},
    {"role": "assistant", "content": "Да, SkyFly Airlines разрешает провоз животных в салоне и багажном отсеке."},

    # Питание на борту
    {"role": "user", "content": "Есть ли бесплатное питание на рейсах SkyFly Airlines?"},
    {"role": "assistant",
     "content": "В тарифе 'Эконом' доступны только напитки. В 'Стандарте' — сэндвич, в 'Премиуме' — горячее блюдо."},

    # Регистрация и посадка
    {"role": "user", "content": "Когда нужно приехать в аэропорт?"},
    {"role": "assistant",
     "content": "Рекомендуется приезжать за 2 часа до внутренних рейсов и 3 часа до международных."},

    # Связь и сервис
    {"role": "user", "content": "Как изменить дату или время рейса?"},
    {"role": "assistant", "content": "Изменения возможны при наличии билета с гибкими условиями."},
]


def ask_deepseek(user_id, message):
    cache_key = f"faq:{message.lower()}"
    cache_response = cache.get(cache_key)
    if cache_response:
        return cache_response.decode('utf-8')

    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_TOKEN}"}

    history = history_cache.get(user_id, [])
    messages = FAQ_CONTEXT.copy()
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    print(history)
    print(messages)

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    cache.setex(cache_key, 3600, answer)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    history_cache[user_id] = history

    print(history_cache)
    return answer


@bot.message_handler(commands=['start'])
async def handler_start(message):
    await bot.send_message(chat_id=message.chat.id, text='Привет! Введи /ask <вопрос>.')


@bot.message_handler(commands=['ask'])
async def handler_question(message):
    user_id = message.chat.id
    question = message.text.replace("/ask", "")
    if not question:
        await bot.send_message(chat_id=user_id, text="Введите вопрос после команды /ask")
        return

    print(question)
    answer = await ask_deepseek(user_id=user_id, message=question)
    await bot.send_message(chat_id=user_id, text=answer)


async def start():
    print("Запуск скрипта")
    await bot.infinity_polling(timeout=10)

asyncio.run(start())



