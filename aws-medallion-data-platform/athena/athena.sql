-- Query 1: Verify Athena

SELECT COUNT(*)
FROM obt;

-- Query 2

SELECT
    flight_class,
    COUNT(*) AS total_bookings
FROM obt
GROUP BY flight_class
ORDER BY total_bookings DESC;

-- Query 3

SELECT
    country,
    COUNT(*) AS total_bookings
FROM obt
GROUP BY country
ORDER BY total_bookings DESC
LIMIT 10;

-- Query 4

SELECT
    ROUND(AVG(ticket_price),2) AS avg_ticket_price
FROM obt;

-- Query 5: Revenue by Country

SELECT
    country,
    ROUND(SUM(ticket_price),2) AS total_revenue,
    COUNT(*) AS total_bookings,
    ROUND(AVG(ticket_price),2) AS avg_ticket_price
FROM obt
GROUP BY country
ORDER BY total_revenue DESC;

-- Purpose: Top revenue generating countries

-- Query 6: Revenue by Flight Class

SELECT
    flight_class,
    ROUND(SUM(ticket_price),2) AS revenue
FROM obt
GROUP BY flight_class
ORDER BY revenue DESC;

-- Purpose: Which ticket class contributes most revenue

-- Query 7: Average Ticket Price by Country

SELECT
    country,
    ROUND(AVG(ticket_price),2) AS avg_price
FROM obt
GROUP BY country
ORDER BY avg_price DESC;

-- Purpose: Premium markets analysis

-- Query 8: Top 10 Airports by Bookings

SELECT
    airport_name,
    COUNT(*) AS bookings
FROM obt
GROUP BY airport_name
ORDER BY bookings DESC
LIMIT 10;

-- Purpose: Most popular airports

-- Query 9: Top 10 Airports by Revenue

SELECT
    airport_name,
    ROUND(SUM(ticket_price),2) AS revenue
FROM obt
GROUP BY airport_name
ORDER BY revenue DESC
LIMIT 10;

-- Purpose: Highest revenue airports

-- Query 10: Monthly Booking Trend

SELECT
    month(booking_date) AS booking_month,
    COUNT(*) AS total_bookings
FROM obt
GROUP BY month(booking_date)
ORDER BY booking_month;

-- Purpose: Booking seasonality

-- Query 11: Monthly Revenue Trend

SELECT
    month(booking_date) AS booking_month,
    ROUND(SUM(ticket_price),2) AS revenue
FROM obt
GROUP BY month(booking_date)
ORDER BY booking_month;

-- Purpose: Revenue trend dashboard

-- Query 12: Passenger Demographics

SELECT
    gender,
    COUNT(*) AS total_passengers
FROM obt
GROUP BY gender;

-- Purpose: Customer segmentation

-- Query 13: Age Group Analysis

SELECT
CASE
    WHEN age < 25 THEN '18-24'
    WHEN age < 35 THEN '25-34'
    WHEN age < 45 THEN '35-44'
    WHEN age < 55 THEN '45-54'
    ELSE '55+'
END AS age_group,
COUNT(*) AS passengers
FROM obt
GROUP BY 1
ORDER BY 1;

-- Purpose: Customer age distribution

-- Query 14: Revenue By Airport

SELECT
    airport_name,
    ROUND(SUM(ticket_price),2) AS total_revenue,
    COUNT(*) AS total_bookings
FROM obt
GROUP BY airport_name
ORDER BY total_revenue DESC;

-- Query 15: Flight Class Summary

SELECT
    flight_class,
    COUNT(*) AS total_bookings,
    ROUND(SUM(ticket_price),2) AS total_revenue,
    ROUND(AVG(ticket_price),2) AS avg_ticket_price
FROM obt
GROUP BY flight_class
ORDER BY total_revenue DESC;

-- Query 16: Monthly Booking Trends

SELECT
    MONTH(booking_date) AS booking_month,
    COUNT(*) AS total_bookings,
    ROUND(SUM(ticket_price),2) AS revenue
FROM obt
GROUP BY MONTH(booking_date)
ORDER BY booking_month;