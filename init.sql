CREATE TABLE IF NOT EXISTS booking_stats (
    org_id INT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_bookings INT NOT NULL,
    total_revenue NUMERIC(15, 2) NOT NULL,
    avg_booking_cost NUMERIC(15, 2) NOT NULL,
    unique_customers INT NOT NULL,
    popular_service VARCHAR(300) NOT NULL,
    most_frequent_client_id INT NOT NULL,
    best_worker_id INT,
    best_worker_rating NUMERIC(15, 2),
    PRIMARY KEY (org_id, period_end)
);