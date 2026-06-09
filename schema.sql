CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    genre VARCHAR(50),
    duration INTEGER,
    language VARCHAR(50)); 

CREATE TABLE theaters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theater_name VARCHAR(100),
    location VARCHAR(100),
    total_seats INTEGER);

CREATE TABLE shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    theater_id INTEGER,
    show_time DATETIME,
    ticket_price FLOAT,
    available_seats INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movies(id),
    FOREIGN KEY(theater_id) REFERENCES theaters(id));

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name VARCHAR(100),
    show_id INTEGER,
    seat_number VARCHAR(20),
    booking_time DATETIME,
    FOREIGN KEY(show_id) REFERENCES shows(id));
