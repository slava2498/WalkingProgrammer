import requests
from telebot import TeleBot

from config import TOKEN as DEEPSEEK_TOKEN, API_KEY_VANTAGE, TELEGRAM_TOKEN

bot = TeleBot(TELEGRAM_TOKEN)


def analyze_stock_trend(crypt_name, pre_text, history_price):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_TOKEN}"}
    message = (
        f"Проанализируй эти данные и дай рекомендации о покупке {crypt_name}. я {pre_text}. не больше 500 символов "
        f"{history_price}"
    )

    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    return data["choices"][0]["message"]["content"]


def get_history_prices(crypt_name):
    url = (
        f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol={crypt_name}"
        f"&market=USD&apikey={API_KEY_VANTAGE}"
    )

    response = requests.get(url)
    data = response.json()
    return data["Time Series (Digital Currency Weekly)"]


@bot.message_handler(commands=['start'])
def handler_start(message):
    bot.send_message(chat_id=message.chat.id, text='Привет! Введи /analyze <тикер>, чтобы получить анализ.')


@bot.message_handler(commands=['analyze'])
def analyze(message):
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(chat_id=message.chat.id, text="Введите тикер, например /analyze TSLA трейдер/инвестор")
        return

    crypt_name = args[1].upper()
    pre_text = args[2].upper()
    history_price = get_history_prices(crypt_name=crypt_name)

    response = analyze_stock_trend(crypt_name=crypt_name, pre_text=pre_text, history_price=str(history_price))
    bot.send_message(chat_id=message.chat.id, text=response)


bot.infinity_polling(timeout=10, long_polling_timeout=30)
