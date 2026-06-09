from pydantic import BaseModel
from datetime import datetime


class MovieCreate(BaseModel):
    title: str
    genre: str
    duration: int
    language: str


class MovieResponse(MovieCreate):
    id: int

    class Config:
        from_attributes = True


class TheaterCreate(BaseModel):
    theater_name: str
    location: str
    total_seats: int


class TheaterResponse(TheaterCreate):
    id: int

    class Config:
        from_attributes = True


class ShowCreate(BaseModel):
    movie_id: int
    theater_id: int
    show_time: datetime
    ticket_price: float


class BookingCreate(BaseModel):
    customer_name: str
    show_id: int
    seat_number: str
