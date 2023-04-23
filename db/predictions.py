from db.get_connection import get_cursor
from datetime import datetime

def save_predictions(predictions: list):
    query = """
        INSERT INTO predictions (region_name, datetime_epoch, prediction)
        VALUES (%s, %s, %s)
        ON CONFLICT (region_name, datetime_epoch)
        DO UPDATE SET prediction = EXCLUDED.prediction
        RETURNING id
    """

    with get_cursor() as cursor:
        for region_name, datetime_epoch, prediction in predictions:
            cursor.execute(query, (region_name, datetime_epoch, prediction))


def get_predictions(region_name: list = [], start_datetime: datetime = datetime(2000,1,1)):
    start_datetime = start_datetime.replace(second=0, microsecond=0, minute=0)
    query = f"SELECT region_name, datetime_epoch, prediction FROM predictions WHERE datetime_epoch>='{start_datetime.strftime('%Y-%m-%d %H:%M:%S')}'"
    if region_name:
        region_name = map(lambda x: f"'{x}'", region_name)
        query += f" AND region_name in ({', '.join(region_name)})"
    query += " ORDER BY datetime_epoch"
    with get_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()