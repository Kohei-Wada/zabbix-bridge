import psycopg2

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )


def get_repository():
    conn = get_db_connection()
    try:
        from repository import HostRepository

        yield HostRepository(conn)
    finally:
        conn.close()
