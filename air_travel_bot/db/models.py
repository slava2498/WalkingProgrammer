import enum

import sqlalchemy as sa

from air_travel_bot.db.init_db import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    chat_id = sa.Column(sa.BIGINT, unique=True, nullable=False)
    username = sa.Column(sa.String, nullable=True)
    first_name = sa.Column(sa.String, nullable=True)
    last_name = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())


class DialogStep(Base):
    __tablename__ = 'dialog_step'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    step_name = sa.Column(sa.String, nullable=False)
    context = sa.Column(sa.JSON, nullable=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())


class Flight(Base):
    __tablename__ = "flights"
    id = sa.Column(sa.Integer, primary_key=True)
    flight_number = sa.Column(sa.String, unique=True)
    origin = sa.Column(sa.String, nullable=False)
    destination = sa.Column(sa.String, nullable=False)
    departure_time = sa.Column(sa.DateTime, nullable=False)
    arrival_time = sa.Column(sa.DateTime, nullable=False)


class SeatClass(enum.Enum):
    economy = 1
    comfort = 2
    business = 3


class Ticket(Base):
    __tablename__ = "tickets"
    id = sa.Column(sa.Integer, primary_key=True)
    flight_id = sa.Column(sa.Integer, sa.ForeignKey("flights.id"), nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    seat_class = sa.Column(sa.Enum(SeatClass), nullable=False)
    seat_number = sa.Column(sa.String, nullable=False)
    available = sa.Column(sa.Boolean, default=True)


class Booking(Base):
    __tablename__ = "bookings"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    ticket_id = sa.Column(sa.Integer, sa.ForeignKey("tickets.id"), nullable=False)
    booked_at = sa.Column(sa.DateTime, server_default=sa.func.now())
