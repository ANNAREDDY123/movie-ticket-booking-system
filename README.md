# movie-ticket-booking-system
Movie Ticket Booking System built using FastAPI, SQLAlchemy, Pydantic, and SQLite. Supports movie management, theater management, show scheduling, and ticket booking APIs.
# Movie Ticket Booking System

## Objective

Backend system to manage:

- Movies
- Theaters
- Shows
- Ticket Bookings

Built using FastAPI, SQLAlchemy, Pydantic and SQLite.

---

## Features

### Movie Management

- Add Movie
- View Movies
- Update Movie
- Delete Movie

### Theater Management

- Add Theater
- View Theaters
- Update Theater
- Delete Theater

### Show Management

- Create Show
- View Shows
- Update Show Timing
- Delete Show

### Ticket Booking

- Book Ticket
- Cancel Ticket
- View Booking History

## Business Rules

- Prevent double booking
- Show must exist before booking
- Cannot book past shows
- Available seats reduce after booking

## SQL Reports

- Most Booked Movie
- Revenue by Movie
- Fully Booked Shows
- Top Customers
- Daily Booking Reports
- Movie Ranking using Window Functions


## Installation

pip install -r requirements.txt

Run:

uvicorn main:app 

Swagger:

http://127.0.0.1:8000/docs


## Files

- schema.sql
- queries.sql
