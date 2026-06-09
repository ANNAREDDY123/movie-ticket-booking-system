
-- 1. Most Booked Movie

SELECT
    m.title,
    COUNT(b.id) AS total_bookings
FROM movies m
JOIN shows s
ON m.id = s.movie_id
JOIN bookings b
ON s.id = b.show_id
GROUP BY m.id,m.title
ORDER BY total_bookings DESC;

-- 2. Total Revenue by Movie

SELECT
    m.title,
    COUNT(b.id) * s.ticket_price AS revenue
FROM movies m
JOIN shows s
ON m.id = s.movie_id
JOIN bookings b
ON s.id = b.show_id
GROUP BY m.id,m.title,s.ticket_price;


-- 3. Fully Booked Shows

SELECT *
FROM shows
WHERE available_seats = 0;

-- 4. Top 5 Customers

SELECT
    customer_name,
    COUNT(*) AS bookings
FROM bookings
GROUP BY customer_name
ORDER BY bookings DESC
LIMIT 5;


-- 5. Daily Booking Report

SELECT
    DATE(booking_time) AS booking_date,
    COUNT(*) AS total_bookings
FROM bookings
GROUP BY DATE(booking_time);


-- 6. Rank Movies By Ticket Sales

SELECT
    movie_name,
    ticket_sales,
    RANK() OVER(
        ORDER BY ticket_sales DESC
    ) AS movie_rank
FROM
( SELECT
        m.title AS movie_name,
        COUNT(b.id) AS ticket_sales
    FROM movies m
    JOIN shows s
    ON m.id=s.movie_id
    JOIN bookings b
    ON s.id=b.show_id
    GROUP BY m.id,m.title
) ranked_movies;
