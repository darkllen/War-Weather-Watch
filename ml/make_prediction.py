import pickle
from sources.prediction_model import get_prediction_data_for_12_hours
from db.predictions import save_predictions
from db.models import get_last_model
import pandas as pd
from datetime import datetime
import os

REGIONS={'Chernivtsi': '1', 'Lutsk': '2', 'Vinnytsia': '3', 'Dnipro': '4', 'Donetsk': '5',
           'Zhytomir': '6', 'Uzhgorod': '7', 'Zaporozhye': '8', 'Kyiv': '9',
           'Kropyvnytskyi': '10', 'Lviv': '12', 'Mykolaiv': '13', 'Odesa': '14',
           'Poltava': '15', 'Rivne': '16', 'Sumy': '17', 'Ternopil': '18', 'Kharkiv': '19',
           'Kherson': '20', 'Khmelnytskyi': '21', 'Cherkasy': '22', 'Chernihiv':'23',
           'Ivano-Frankivsk': '24'}


def update_prediction_for_next_12_hours():
    regions_reverse = {v:k for k, v in REGIONS.items()}
    model = get_last_model()
    data = get_prediction_data_for_12_hours(os.environ.get("WEATHER_API_KEY"), REGIONS)
    data = data.apply(pd.to_numeric, errors='coerce')
    data.fillna(0, inplace=True)
    pred = model.predict(data)
    data['is_alarm'] = pred
    data = data[['region_id', 'day_datetimeEpoch', 'is_alarm']]
    data['region_id'] = data['region_id'].apply(lambda x: regions_reverse[str(int(x))])
    data["day_datetimeEpoch"] = data["day_datetimeEpoch"].apply(lambda x: datetime.fromtimestamp(x))
    return data


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    data = update_prediction_for_next_12_hours()
    data_vals = data.values.tolist()
    save_predictions(data_vals)