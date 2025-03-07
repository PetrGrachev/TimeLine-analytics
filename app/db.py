import psycopg2

def get_db_connection(config):
    return psycopg2.connect(**config)