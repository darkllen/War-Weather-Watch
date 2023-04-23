from contextlib import contextmanager
import psycopg2
import os

@contextmanager
def get_cursor():
    conn = psycopg2.connect(
        host=os.environ.get("HOST"),
        port=os.environ.get("PORT"),
        database=os.environ.get("DATABASE"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )

    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()


