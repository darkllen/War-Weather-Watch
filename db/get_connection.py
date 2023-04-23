from contextlib import contextmanager
import psycopg2
import os

@contextmanager
def get_cursor():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        database=os.environ.get("DATABASE"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )

    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()


