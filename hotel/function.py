from datetime import date
from typing import NamedTuple, List, Tuple


class Room(NamedTuple):
    room_id: int
    room_type: str
    base_price: int
    is_luxury: bool = False
    bookings: List[Tuple[date, date]] = []


def is_available(room: Room, start_date: date, end_date: date) -> bool:
    return all(not(start_date < bookings_end and end_date > booking_start) for (booking_start, bookings_end) in room.bookings)


def calculate_price(room: Room, start_date: date, end_date: date, guests: int) -> float:
    days = (end_date - start_date).days
    price = room.base_price * days
    if room.is_luxury:
        price *= 1.25
    if guests > 2:
        price += (guests - 2) * 500 * days
    return price


def search_available_rums(rooms: [Room], start_date: date, end_date: date) -> List[Room]:
    return list(filter(lambda r: is_available(r, start_date, end_date), rooms))


rooms = [
    Room(101, 'single', 3000),
    Room(102, 'double', 5000),
    Room(201, 'suite', 8000, True, [(date(2025, 5, 2), date(2025, 5, 4))]),
]


start = date(2025, 5, 1)
end = date(2025, 5, 5)

available = search_available_rums(rooms, start, end)

for room in available:
    print(f"Комната {room.room_id}: {(calculate_price(room, start, end, 3))} рублей")