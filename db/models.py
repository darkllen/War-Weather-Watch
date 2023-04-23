from db.get_connection import get_cursor
import pickle

def save_model(model_path, model_name):

    query = """
        INSERT INTO models (model_name, model_file)
        VALUES (%s, %s)
    """

    with open(model_path, 'rb') as f:
        file_contents = f.read()

    with get_cursor() as cursor:
        cursor.execute(query, (model_name, file_contents))


def get_last_model():

    query = "SELECT model_file FROM models ORDER BY created_at DESC LIMIT 1"

    with get_cursor() as cursor:
        cursor.execute(query)

        result = cursor.fetchone()
        if result:
            last_model_file = result[0]
            return pickle.loads(last_model_file)

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    # save_model('', '')
    model = get_last_model()
