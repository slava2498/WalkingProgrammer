import asyncio
import datetime
from typing import Dict, Optional, List

import sqlalchemy as sa
import telebot
from telebot.async_telebot import AsyncTeleBot

from air_travel_bot.config import TOKEN
from air_travel_bot.db.init_db import SessionLocal, redis_client
from db.models import User, Flight, Booking, Ticket, DialogStep, SeatClass

bot = AsyncTeleBot(TOKEN)

class_map = {
    'эконом': SeatClass.economy,
    'комфорт': SeatClass.comfort,
    'бизнес': SeatClass.business,
}


@bot.message_handler(commands=['start'])
async def handle_start(message):
    async with SessionLocal() as session:
        user = await session.execute(
            sa.select(User.id)
            .select_from(User)
            .where(User.chat_id == message.chat.id)
        )
        if not user.first():
            await session.execute(
                sa.insert(User)
                .values({
                    User.chat_id: message.chat.id,
                    User.username: message.chat.username,
                    User.first_name: message.chat.first_name,
                    User.last_name: message.chat.last_name,
                })
            )
            await session.commit()

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🎟 Забронировать билет')
        markup.add('✈ Поиск билетов', '📋 Мои бронирования')
        markup.add('ℹ️ FAQ', '👤 Личный кабинет')

        await bot.send_message(
            chat_id=message.chat.id,
            text="Добро пожаловать в SkyFly Airlines!",
            reply_markup=markup
        )


@bot.message_handler(func=lambda message: message.text == 'ℹ️ FAQ')
async def handle_faq(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Раздел FAQ пока в разработке",
    )


async def search_flights(
    origin: str,
    destination: str,
    departure_time: datetime.date,
    arrival_time: Optional[datetime.date],
    seat_class: SeatClass,
    price: int
) -> List:
    filters = [
        Flight.origin == origin,
        Flight.destination == destination,
        Flight.departure_time.cast(sa.Date) >= departure_time,
        Ticket.seat_class == seat_class,
        Ticket.price <= price,
        Ticket.available.is_(sa.true()),
    ]
    if arrival_time is not None:
        filters.append(Flight.arrival_time.cast(sa.Date) >= arrival_time)

    async with SessionLocal() as session:
        flight_res = await session.execute(
            sa.select(
                Flight.flight_number,
                Flight.departure_time,
                Flight.arrival_time,
                Flight.origin,
                Flight.destination,
                Ticket.seat_class,
                Ticket.price
            )
            .select_from(Flight)
            .join(Ticket, Ticket.flight_id == Flight.id)
            .where(sa.and_(*filters))
        )
        flights = flight_res.all()

        if not flights:
            return []

        return flights


@bot.message_handler(func=lambda message: message.text == '✈ Поиск билетов')
async def handle_search(message):
    redis_client.set(f"search_step:{message.chat.id}", "city_from")
    await bot.send_message(chat_id=message.chat.id, text="Введите город отправления:")


@bot.message_handler(func=lambda msg: redis_client.get(f"search_step:{msg.chat.id}") == "city_from")
async def handle_city_from(message):
    redis_client.set(f"user:{message.chat.id}:city_from", message.text)
    redis_client.set(f"search_step:{message.chat.id}", "city_to")
    await bot.send_message(chat_id=message.chat.id, text="Введите город назначения:")


@bot.message_handler(func=lambda msg: redis_client.get(f"search_step:{msg.chat.id}") == "city_to")
async def handle_city_to(message):
    redis_client.set(f"user:{message.chat.id}:city_to", message.text)
    redis_client.set(f"search_step:{message.chat.id}", "departure_date")
    await bot.send_message(chat_id=message.chat.id, text="Введите дату вылета (в формате ГГГГ-ММ-ДД. 2025-05-17)")


@bot.message_handler(func=lambda msg: redis_client.get(f"search_step:{msg.chat.id}") == "departure_date")
async def handle_departure_date(message):
    redis_client.set(f"user:{message.chat.id}:departure_date", message.text)
    redis_client.set(f"search_step:{message.chat.id}", "arrival_date")
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите дату прилета (можно пропустить, введя '-'), в формате ГГГГ-ММ-ДД. 2025-05-17"
    )


@bot.message_handler(func=lambda msg: redis_client.get(f"search_step:{msg.chat.id}") == "arrival_date")
async def handle_arrival_date(message):
    step_context = ""
    if message.text != "-":
        step_context = message.text

    redis_client.set(f"user:{message.chat.id}:arrival_date", step_context)
    redis_client.set(f"search_step:{message.chat.id}", "seat_class")
    await bot.send_message(chat_id=message.chat.id, text="Выберите класс места (эконом/комфорт/бизнес)")


@bot.message_handler(func=lambda msg: redis_client.get(f"search_step:{msg.chat.id}") == "seat_class")
async def handle_seat_class(message):
    if not class_map.get(message.text):
        await bot.send_message(chat_id=message.chat.id, text="Доступные классы: эконом/комфорт/бизнес")
        return

    redis_client.set(f"user:{message.chat.id}:seat_class", message.text)
    redis_client.set(f"search_step:{message.chat.id}", "max_price")
    await bot.send_message(
        chat_id=message.chat.id,
        text="Укажите максимальную цену за билет (в рублях)"
    )


def clear_search_state(chat_id):
    keys = [
        f"user:{chat_id}:city_from",
        f"user:{chat_id}:city_to",
        f"user:{chat_id}:departure_date",
        f"user:{chat_id}:arrival_date",
        f"user:{chat_id}:seat_class",
        f"user:{chat_id}:max_price",
        f"search_step:{chat_id}"
    ]
    redis_client.delete(*keys)


@bot.message_handler(func=lambda msg: redis_client.get(f"search_step:{msg.chat.id}") == "max_price")
async def handle_seat_class(message):
    redis_client.set(f"user:{message.chat.id}:max_price", message.text)

    city_from = redis_client.get(f"user:{message.chat.id}:city_from")
    city_to = redis_client.get(f"user:{message.chat.id}:city_to")
    departure_date = redis_client.get(f"user:{message.chat.id}:departure_date")
    arrival_date = redis_client.get(f"user:{message.chat.id}:arrival_date")
    seat_class = redis_client.get(f"user:{message.chat.id}:seat_class")
    max_price = redis_client.get(f"user:{message.chat.id}:max_price")

    flights = await search_flights(
        origin=city_from,
        destination=city_to,
        departure_time=datetime.datetime.strptime(departure_date, "%Y-%m-%d").date(),
        arrival_time=datetime.datetime.strptime(arrival_date, "%Y-%m-%d").date() if arrival_date else None,
        seat_class=class_map[seat_class],
        price=int(max_price)
    )
    if not flights:
        await bot.send_message(chat_id=message.chat.id, text="Рейсов не найдено")

    result_text = []
    for flight in flights:
        result_text.append(
            f"✈ Рейс {flight.flight_number}\n"
            f"{flight.origin} -> {flight.destination}\n"
            f"{flight.departure_time.strftime('%d.%m %H:%M')} -> {flight.arrival_time.strftime('%d.%m %H:%M')}\n"
            f"Класс {flight.seat_class.name}, Цена: {flight.price}₽"
        )

    await bot.send_message(chat_id=message.chat.id, text="\n---\n".join(result_text))
    clear_search_state(chat_id=message.chat.id)


async def save_dialog_step(chat_id: str, step_name: str, context: Dict):
    async with SessionLocal() as session:
        user_q = await session.execute(
            sa.select(User.id)
            .select_from(User)
            .where(User.chat_id == chat_id)
        )
        user = user_q.first()

        dialog = await session.execute(
            sa.select(DialogStep.id)
            .select_from(DialogStep)
            .where(DialogStep.user_id == user.id)
        )

        if not dialog.first():
            await session.execute(
                sa.insert(DialogStep)
                .values({
                    DialogStep.user_id: user.id,
                    DialogStep.context: context,
                    DialogStep.step_name: step_name,
                })
            )
        else:
            await session.execute(
                sa.update(DialogStep)
                .values({
                    DialogStep.context: context,
                    DialogStep.step_name: step_name,
                })
                .where(DialogStep.user_id == user.id)
            )

        await session.commit()


async def get_dialog_step(message) -> Optional[str]:
    async with SessionLocal() as session:
        dialog_query = await session.execute(
            sa.select(DialogStep.step_name)
            .select_from(DialogStep)
            .join(User, User.id == DialogStep.user_id)
            .where(User.chat_id == message.chat.id)
        )
        dialog = dialog_query.first()
        if not dialog:
            return None

        return dialog.step_name


async def get_dialog_context(chat_id: str) -> Optional[Dict]:
    async with SessionLocal() as session:
        dialog_query = await session.execute(
            sa.select(DialogStep.context)
            .select_from(DialogStep)
            .join(User, User.id == DialogStep.user_id)
            .where(User.chat_id == chat_id)
        )
        dialog = dialog_query.first()
        if not dialog:
            return None

        return dialog.context


async def get_seats(flight_number: str, seat_class: str) -> List[str]:
    async with SessionLocal() as session:
        ticket_query = await session.execute(
            sa.select(Ticket.seat_number)
            .select_from(Ticket)
            .join(Flight, Flight.id == Ticket.flight_id)
            .where(sa.and_(
                Flight.flight_number == flight_number,
                Ticket.seat_class == seat_class,
                Ticket.available.is_(sa.true()),
            ))
        )

        tickets = ticket_query.all()
        if not tickets:
            return []

        return [ticket.seat_number for ticket in tickets]


async def booking(seat_number: str, chat_id: str):
    async with SessionLocal() as session:
        await session.execute(
            sa.update(Ticket)
            .values({Ticket.available: sa.false()})
            .where(Ticket.seat_number == seat_number)
        )

        user_q = await session.execute(
            sa.select(User.id)
            .select_from(User)
            .where(User.chat_id == chat_id)
        )
        user = user_q.first()

        ticket_q = await session.execute(
            sa.select(Ticket.id)
            .select_from(Ticket)
            .where(Ticket.seat_number == seat_number)
        )
        ticket = ticket_q.first()

        await session.execute(
            sa.insert(Booking)
            .values({
                Booking.user_id: user.id,
                Booking.ticket_id: ticket.id,
            })
        )

        await session.commit()


async def delete_dialog(chat_id: str):
    async with SessionLocal() as session:
        user_q = await session.execute(
            sa.select(User.id)
            .select_from(User)
            .where(User.chat_id == chat_id)
        )
        user = user_q.first()

        await session.execute(
            sa.delete(DialogStep)
            .where(DialogStep.user_id == user.id)
        )
        await session.commit()


@bot.message_handler(func=lambda message: message.text == '🎟 Забронировать билет')
async def handle_flight_number(message):
    await save_dialog_step(chat_id=message.chat.id, step_name='select_flight', context={})
    await bot.send_message(chat_id=message.chat.id, text="Введите номер рейса")


@bot.message_handler(func=get_dialog_step)
async def handle_dialog_control(message):
    step_name = await get_dialog_step(message)
    if step_name == "select_flight":
        context = {'flight_number': message.text}
        await save_dialog_step(chat_id=message.chat.id, step_name='select_class', context=context)
        await bot.send_message(chat_id=message.chat.id, text="Выберите класс места (эконом/комфорт/бизнес)")

    elif step_name == "select_class":
        context = await get_dialog_context(chat_id=message.chat.id)
        context['seat_class'] = message.text

        seats = await get_seats(flight_number=context['flight_number'], seat_class=class_map[message.text])
        if not seats:
            await bot.send_message(chat_id=message.chat.id, text="Свободных мест нет для этого класса")
            await delete_dialog(chat_id=message.chat.id)
            return

        await save_dialog_step(chat_id=message.chat.id, step_name='select_seat', context=context)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Свободные места: {', '.join(seats)}\nВыберите место для бронирования"
        )

    elif step_name == "select_seat":
        await booking(chat_id=message.chat.id, seat_number=message.text)
        await bot.send_message(
            chat_id=message.chat.id,
            text="✅ Билет успешно забронирован!"
        )
        await delete_dialog(chat_id=message.chat.id)


@bot.message_handler(func=lambda message: message.text == '📋 Мои бронирования')
async def handle_bookings(message):
    async with SessionLocal() as session:
        booking_res = await session.execute(
            sa.select(
                Flight.flight_number,
                Flight.departure_time,
                Flight.arrival_time,
                Flight.origin,
                Flight.destination,
                Ticket.seat_class,
                Ticket.price
            )
            .select_from(Booking)
            .join(Ticket, Ticket.id == Booking.ticket_id)
            .join(Flight, Flight.id == Ticket.flight_id)
            .join(User, User.id == Booking.user_id)
            .where(User.chat_id == message.chat.id)
        )
        bookings = booking_res.all()
        if not bookings:
            await bot.send_message(chat_id=message.chat.id, text="У вас пока нет бронирований")
            return

        result_text = []
        for booking in bookings:
            result_text.append(
                f"✅ Рейс {booking.flight_number}\n"
                f"{booking.origin} -> {booking.destination}\n"
                f"{booking.departure_time.strftime('%d.%m %H:%M')} -> {booking.arrival_time.strftime('%d.%m %H:%M')}\n"
                f"Класс {booking.seat_class.name}, Цена: {booking.price}₽"
            )

        await bot.send_message(chat_id=message.chat.id, text="\n---\n".join(result_text))


@bot.message_handler(func=lambda message: message.text == '👤 Личный кабинет')
async def handle_profile(message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Личный кабинет",
    )


async def main():
    await bot.infinity_polling(timeout=10)


asyncio.run(main())
