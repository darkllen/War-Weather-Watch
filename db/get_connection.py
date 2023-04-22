from contextlib import contextmanager
import psycopg2

HOST=''
DATABASE=''
USER=''
PASSWORD=''
PORT=5432

@contextmanager
def get_cursor():
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )

    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()


