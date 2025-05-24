import requests
from telebot import TeleBot

from config import TOKEN as DEEPSEEK_TOKEN, TELEGRAM_TOKEN

bot = TeleBot(TELEGRAM_TOKEN)


cache = {}
history_cache = {}

FEW_SHOW_EXAMPLES = [
    {"role": "user", "content": "Когда был основан Рим?"},
    {"role": "assistant", "content": "Ответ: 753 год до н.э."},
    {"role": "user", "content": "Кто был первым императором Рима?"},
    {"role": "assistant", "content": "Ответ: Октавиан Август"}
]


def ask_deepseek(user_id, message):
    print(cache)
    if message in cache:
        return cache[message]

    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_TOKEN}"}

    history = history_cache.get(user_id, [])
    messages = [{"role": "system", "content": "Ты историк. Отвечай кратко, начиная с `Ответ:`"}]
    messages.extend(FEW_SHOW_EXAMPLES)
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

    cache[message] = answer
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    history_cache[user_id] = history

    print(history_cache)
    return answer


@bot.message_handler(commands=['start'])
def handler_start(message):
    bot.send_message(chat_id=message.chat.id, text='Привет! Введи /ask <вопрос> или очисть свой кеш /clear.')


@bot.message_handler(commands=['ask'])
def handler_question(message):
    user_id = message.chat.id
    question = message.text.replace("/ask", "")
    if not question:
        bot.send_message(chat_id=user_id, text="Введите вопрос после команды /ask")
        return

    print(question)
    answer = ask_deepseek(user_id=user_id, message=question)
    bot.send_message(chat_id=user_id, text=answer)


@bot.message_handler(commands=['clear'])
def clear_history(message):
    user_id = message.chat.id
    history_cache.pop(user_id, None)
    print(history_cache)
    bot.send_message(chat_id=user_id, text="История диалога очищена")


bot.infinity_polling(timeout=10, long_polling_timeout=30)
