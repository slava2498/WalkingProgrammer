from datetime import date


class Room:
    def __init__(self, room_id, room_type, base_price, is_luxury=False):
        self.room_id = room_id
        self.room_type = room_type
        self.base_price = base_price
        self.is_luxury = is_luxury
        self.bookings = []

    def is_available(self, start_date, end_date):
        for (booking_start, bookings_end) in self.bookings:
            if start_date < bookings_end and end_date > booking_start:
                return False
        return True

    def book(self, start_date, end_date):
        self.bookings.append((start_date, end_date))

    def calculate_price(self, start_date, end_date, guests):
        days = (end_date - start_date).days
        price = self.base_price * days
        if self.is_luxury:
            price *= 1.25
        if guests > 2:
            price += (guests - 2) * 500 * days
        return price


class Hotel:
    def __init__(self, rooms):
        self.rooms = rooms

    def search(self, start_date, end_date, guests):
        return [
            (room, room.calculate_price(start_date, end_date, guests))
            for room in self.rooms
            if room.is_available(start_date=start_date, end_date=end_date)
        ]


rooms = [
    Room(101, 'single', 3000),
    Room(102, 'double', 5000),
    Room(201, 'suite', 8000, is_luxury=True),
]

hotel = Hotel(rooms=rooms)

start = date(2025, 5, 1)
end = date(2025, 5, 5)

available = hotel.search(start, end, guests=3)

for (room, price) in available:
    print(f"Комната {room.room_id}: {price} рублей")

    if price < 15000:
        room.book(start, end)

available = hotel.search(start, end, guests=3)
for (room, price) in available:
    print(f"Комната {room.room_id}: {price} рублей")