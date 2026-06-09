from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal, engine, Base
from models import Movie, Theater, Show, Booking
from schemas import *

app = FastAPI(title="Movie Ticket Booking System")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Movie Ticket Booking System Running"}


# MOVIE APIs


@app.post("/movies")
def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int,
                 movie: MovieCreate,
                 db: Session = Depends(get_db)):

    db_movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not db_movie:
        raise HTTPException(404, "Movie not found")

    db_movie.title = movie.title
    db_movie.genre = movie.genre
    db_movie.duration = movie.duration
    db_movie.language = movie.language

    db.commit()

    return {"message": "Movie updated"}


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int,
                 db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not movie:
        raise HTTPException(404, "Movie not found")

    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted"}



# THEATER APIs

@app.post("/theaters")
def add_theater(theater: TheaterCreate,
                db: Session = Depends(get_db)):

    db_theater = Theater(**theater.model_dump())

    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)

    return db_theater


@app.get("/theaters")
def get_theaters(db: Session = Depends(get_db)):
    return db.query(Theater).all()


@app.put("/theaters/{theater_id}")
def update_theater(theater_id: int,
                   theater: TheaterCreate,
                   db: Session = Depends(get_db)):

    db_theater = db.query(Theater).filter(
        Theater.id == theater_id
    ).first()

    if not db_theater:
        raise HTTPException(404, "Theater not found")

    db_theater.theater_name = theater.theater_name
    db_theater.location = theater.location
    db_theater.total_seats = theater.total_seats

    db.commit()

    return {"message": "Theater updated"}


@app.delete("/theaters/{theater_id}")
def delete_theater(theater_id: int,
                   db: Session = Depends(get_db)):

    theater = db.query(Theater).filter(
        Theater.id == theater_id
    ).first()

    if not theater:
        raise HTTPException(404, "Theater not found")

    db.delete(theater)
    db.commit()

    return {"message": "Theater deleted"}


# SHOW APIs

@app.post("/shows")
def create_show(show: ShowCreate,
                db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(
        Movie.id == show.movie_id
    ).first()

    theater = db.query(Theater).filter(
        Theater.id == show.theater_id
    ).first()

    if not movie:
        raise HTTPException(404, "Movie not found")

    if not theater:
        raise HTTPException(404, "Theater not found")

    db_show = Show(
        movie_id=show.movie_id,
        theater_id=show.theater_id,
        show_time=show.show_time,
        ticket_price=show.ticket_price,
        available_seats=theater.total_seats
    )

    db.add(db_show)
    db.commit()
    db.refresh(db_show)

    return db_show


@app.get("/shows")
def get_shows(db: Session = Depends(get_db)):
    return db.query(Show).all()


@app.put("/shows/{show_id}")
def update_show(show_id: int,
                show: ShowCreate,
                db: Session = Depends(get_db)):

    db_show = db.query(Show).filter(
        Show.id == show_id
    ).first()

    if not db_show:
        raise HTTPException(404, "Show not found")

    db_show.show_time = show.show_time
    db_show.ticket_price = show.ticket_price

    db.commit()

    return {"message": "Show updated"}


@app.delete("/shows/{show_id}")
def delete_show(show_id: int,
                db: Session = Depends(get_db)):

    show = db.query(Show).filter(
        Show.id == show_id
    ).first()

    if not show:
        raise HTTPException(404, "Show not found")

    db.delete(show)
    db.commit()

    return {"message": "Show deleted"}


# BOOKING APIs

@app.post("/bookings")
def book_ticket(booking: BookingCreate,
                db: Session = Depends(get_db)):

    show = db.query(Show).filter(
        Show.id == booking.show_id
    ).first()

    if not show:
        raise HTTPException(
            404,
            "Show not found"
        )

    if show.show_time < datetime.utcnow():
        raise HTTPException(
            400,
            "Cannot book past show"
        )

    existing_booking = db.query(Booking).filter(
        Booking.show_id == booking.show_id,
        Booking.seat_number == booking.seat_number
    ).first()

    if existing_booking:
        raise HTTPException(
            400,
            "Seat already booked"
        )

    if show.available_seats <= 0:
        raise HTTPException(
            400,
            "No seats available"
        )

    new_booking = Booking(
        customer_name=booking.customer_name,
        show_id=booking.show_id,
        seat_number=booking.seat_number
    )

    show.available_seats -= 1

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


@app.get("/bookings")
def booking_history(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int,
                   db: Session = Depends(get_db)):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            404,
            "Booking not found"
        )

    show = db.query(Show).filter(
        Show.id == booking.show_id
    ).first()

    show.available_seats += 1

    db.delete(booking)
    db.commit()

    return {"message": "Booking cancelled"}
