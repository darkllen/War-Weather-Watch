from db.get_connection import get_cursor

def get_last_words():

    query = "SELECT words_vector FROM vector ORDER BY created_at DESC LIMIT 1"

    with get_cursor() as cursor:
        cursor.execute(query)

        result = cursor.fetchone()
        if result:
            last_vector = result[0]
            return last_vector

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    vector = get_last_words()