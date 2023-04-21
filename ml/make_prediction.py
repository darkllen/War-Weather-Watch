import pickle
from sources.prediction_model import get_prediction_data_for_12_hours
import pandas as pd
from datetime import datetime

MODEL_PATH = 'data/1__decision_tree_classifier__v5.pkl'
RES_PREDICTION_PATH = "data/predictions.csv"
TEST_CSV_PATH = "data/test.csv"
API_KEY = ''
REGIONS={'Chernivtsi': '1','Lutsk': '2', 'Vinnytsia': '3', 'Dnipro': '4', 'Donets': '5',
           'Zhytomir': '6', 'Uzhgorod': '7', 'Zaporozhye': '8', 'Kyiv': '9',
           'Kropyvnytskyi': '10', 'Lviv': '12', 'Mykolaiv': '13', 'Odesa': '14',
           'Poltava': '15', 'Rivne': '16', 'Sumy': '17', 'Ternopil': '18', 'Kharkiv': '19',
           'Kherson': '20', 'Khmelnytskyi': '21', 'Cherkasy': '22', 'Chernihiv':'23',
           'Ivano-Frankivsk': '24'}


def update_prediction_for_next_12_hours():
    regions_reverse = {v:k for k, v in REGIONS.items()}
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f) 
        data = get_prediction_data_for_12_hours(TEST_CSV_PATH, API_KEY, REGIONS)
        data = data.apply(pd.to_numeric, errors='coerce')
        data.fillna(0, inplace=True)
        pred = model.predict(data)
        data['is_alarm'] = pred
        data = data[['region_id', 'day_datetimeEpoch', 'is_alarm']]
        data['region_id'] = data['region_id'].apply(lambda x: regions_reverse[str(int(x))])
        data["day_datetimeEpoch"] = data["day_datetimeEpoch"].apply(lambda x: datetime.fromtimestamp(x))
        return data


if __name__ == "__main__":
    data = update_prediction_for_next_12_hours()
    data.to_csv(RES_PREDICTION_PATH, index=False, sep=";")