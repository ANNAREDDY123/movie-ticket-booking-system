from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    genre = Column(String)
    duration = Column(Integer)
    language = Column(String)


class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True)

    theater_name = Column(String)
    location = Column(String)
    total_seats = Column(Integer)


class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)

    movie_id = Column(Integer, ForeignKey("movies.id"))
    theater_id = Column(Integer, ForeignKey("theaters.id"))

    show_time = Column(DateTime)
    ticket_price = Column(Float)

    available_seats = Column(Integer)

    movie = relationship("Movie")
    theater = relationship("Theater")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String)

    show_id = Column(Integer, ForeignKey("shows.id"))

    seat_number = Column(String)

    booking_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    show = relationship("Show")
