CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    uuid VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    passwd_hash TEXT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    telephone VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    about TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    is_delete BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS users_verify (
    user_verify_id SERIAL PRIMARY KEY,
    user_id INT,
    code VARCHAR(6) NOT NULL,
    expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS orgs (
    org_id SERIAL PRIMARY KEY,
    uuid VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    passwd_hash TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    rating NUMERIC(3, 2) DEFAULT 0.00,
    type VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address VARCHAR(300) NOT NULL,
    telephone VARCHAR(255),
    lat FLOAT NOT NULL,
    long FLOAT NOT NULL,
    about TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    is_delete BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS showcase (
    url VARCHAR(100) PRIMARY KEY,
    type VARCHAR(100),
    org_id INT NOT NULL,
    FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE
);
CREATE INDEX idx_showcase_org_id ON showcase (org_id);
CREATE TABLE IF NOT EXISTS timetables (
    timetable_id SERIAL PRIMARY KEY,
    org_id INT NOT NULL,
    weekday INT NOT NULL,
    open TIMESTAMP NOT NULL,
    close TIMESTAMP NOT NULL,
    break_start TIMESTAMP NOT NULL,
    break_end TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS orgs_verify (
    org_verify_id SERIAL PRIMARY KEY,
    org_id INT NOT NULL,
    code VARCHAR(6) NOT NULL,
    expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS services (
    service_id SERIAL PRIMARY KEY,
    org_id INT,
    name VARCHAR(300) NOT NULL,
    cost NUMERIC(15, 2) NOT NULL,
    description VARCHAR(400),
    FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
    is_delete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS workers (
    worker_id SERIAL PRIMARY KEY,
    uuid VARCHAR(50),
    org_id INT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    position VARCHAR(300),
    session_duration INT,
    degree VARCHAR(300),
    FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
    is_delete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS worker_services (
    worker_id INT,
    service_id INT,
    PRIMARY KEY (worker_id, service_id),
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE,
    is_delete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS worker_schedules (
    worker_schedule_id SERIAL PRIMARY KEY,
    org_id INT,
    worker_id INT,
    weekday INT,
    start TIMESTAMP,
    over TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES orgs(org_id) ON DELETE CASCADE,
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id) ON DELETE CASCADE,
    is_delete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS slots (
    slot_id SERIAL PRIMARY KEY,
    worker_schedule_id INT,
    worker_id INT,
    date DATE,
    session_begin TIMESTAMP,
    session_end TIMESTAMP,
    busy BOOLEAN,
    FOREIGN KEY (worker_schedule_id) REFERENCES worker_schedules(worker_schedule_id),
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS records (
    record_id SERIAL PRIMARY KEY,
    reviewed BOOLEAN DEFAULT FALSE,
    slot_id INT,
    service_id INT,
    worker_id INT,
    user_id INT,
    org_id INT,
    FOREIGN KEY (slot_id) REFERENCES slots(slot_id),
    FOREIGN KEY (service_id) REFERENCES services(service_id),
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (org_id) REFERENCES orgs(org_id),
    UNIQUE (slot_id),
    is_canceled BOOL DEFAULT FALSE,
    cancel_reason VARCHAR(300) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS feedbacks (
    feedback_id SERIAL,
    record_id INT,
    stars INT,
    feedback TEXT,
    FOREIGN KEY (record_id) REFERENCES records(record_id) ON DELETE CASCADE,
    CONSTRAINT unique_record_id UNIQUE(record_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);