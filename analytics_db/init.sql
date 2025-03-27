CREATE TABLE IF NOT EXISTS booking_stats (
    org_id INT NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_bookings INT NOT NULL,
    total_revenue NUMERIC(15, 2) NOT NULL,
    avg_booking_cost NUMERIC(15, 2) NOT NULL,
    unique_customers INT NOT NULL,
    popular_service_id INT,
    most_frequent_client_id INT,
    best_worker_id INT,
    best_worker_rating NUMERIC(15, 2),
    worst_worker_id INT,
    worst_worker_rating NUMERIC(15, 2),
    best_service_id INT,
    best_service_rating NUMERIC(15, 2),
    worst_service_id INT,
    worst_service_rating NUMERIC(15, 2),
    PRIMARY KEY (org_id, period_end)
);
CREATE TABLE IF NOT EXISTS booking_distribution (
    org_id INT,
    day_of_week INT,
    hour INT,
    total_bookings INT,
    period_start DATE,
    period_end DATE,
    PRIMARY KEY (
        org_id,
        day_of_week,
        hour,
        period_start,
        period_end
    )
);
CREATE TABLE IF NOT EXISTS income_distribution (
    org_id INT,
    day_of_week INT,
    total_bookings INT,
    total_income INT,
    period_start DATE,
    period_end DATE,
    PRIMARY KEY (
        org_id,
        day_of_week,
        period_start,
        period_end
    )
);
CREATE TABLE IF NOT EXISTS cancellations (
    org_id INT,
    canceled_records INT,
    cancellation_percentage INT,
    most_common_cancel_reason VARCHAR(300),
    period_start DATE,
    period_end DATE,
    PRIMARY KEY (
        org_id,
        period_start,
        period_end
    )
);
CREATE TABLE IF NOT EXISTS workers_workload (
    org_id INT,
    worker_id INT,
    busy_slots INT,
    total_slots INT,
    workload_percentage NUMERIC(15, 2),
    period_start DATE,
    period_end DATE,
    PRIMARY KEY (
        org_id,
        worker_id,
        period_start,
        period_end
    )
);
CREATE TABLE IF NOT EXISTS feedback_analysis (
    org_id INT,
    period_start DATE,
    period_end DATE,
    positive_keywords JSONB,
    negative_keywords JSONB,
    PRIMARY KEY(org_id, period_start, period_end)
);