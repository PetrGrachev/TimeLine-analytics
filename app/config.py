import os

class Config:
    ANALYTICS_DB_CONFIG = {
        "dbname": os.getenv("DB_NAME", "analytics_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "secret"),
        "host": os.getenv("DB_HOST", "postgres_analytics"),
        "port": os.getenv("DB_PORT", "5432")
    }

    MAIN_DB_CONFIG = {
        "dbname": os.getenv("MAIN_DB_NAME", "main_db"),
        "user": os.getenv("MAIN_DB_USER", "postgres"),
        "password": os.getenv("MAIN_DB_PASSWORD", "secret"),
        "host": os.getenv("MAIN_DB_HOST", "postgres_main"),
        "port": os.getenv("MAIN_DB_PORT", "5432")
    }