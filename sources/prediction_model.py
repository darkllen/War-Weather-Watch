import csv
import time
import ast
import requests
import datetime
from datetime import date, timedelta
from sources.getISWnews import get_isw_news_for_date
import json
import pandas as pd


def get_prediction_data_for_12_hours(test_csv_path, api_key, regions):
    with open(test_csv_path, encoding="utf-8") as file_obj:
        reader_obj = csv.reader(file_obj, delimiter=';')
        row0=next(reader_obj, None)
        rowdict=row0[19::]


    yesterday = date.today() - timedelta(days=1)
    from_date = datetime.date(yesterday.year, yesterday.month, yesterday.day)
    till_date = datetime.date(yesterday.year, yesterday.month, yesterday.day)

    isw_news = get_isw_news_for_date(from_date, till_date)
    
    not_in = {v: 0 for v in rowdict if v not in isw_news['news'].apply(pd.Series)}
    not_in = pd.Series([not_in])
    not_in = not_in.apply(pd.Series)

    series =isw_news['news'].apply(pd.Series)
    series = series.loc[:, series.columns.isin(rowdict)]
    series = pd.concat([series, not_in], axis=1)
    isw_news = pd.concat([isw_news.drop(['news', 'date'], axis=1), series], axis=1)
    
    isw_news['key_merge'] = 1

    res = []
    for region_name, region_id  in regions.items():
        forecast=pd.DataFrame(get_weather(api_key, region_name+',Ukraine'))
        forecast['key_merge'] = 1
  
        data = pd.merge(forecast, isw_news, on ='key_merge').drop("key_merge", 1)
        data['region_id'] = region_id
        res.append(data)

    res = pd.concat(res)
    order = [r for r in row0 if r in res.columns]
    res = res[order]
    return res


now = datetime.datetime.now()
rounded_hour = (now.replace(second=0, microsecond=0, minute=0, hour=now.hour)
                 + datetime.timedelta(hours=1))
print(rounded_hour)

BASE_URL='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

def get_weather(api_key, city = 'Kyiv'):
    url = f'{BASE_URL}/{city}'
    params = {
        'unitGroup': 'metric',
        'key': f'{api_key}',
        'include': 'hours',
        'aggregateHours': '1',
        'hoursAhead':'12'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['days'][0]['hours']
        hourly_forecast = [
            {
                'day_datetimeEpoch': hour['datetimeEpoch'],
                'hour_temp': hour['temp'],
                'hour_humidity': hour['humidity'],
                'hour_snow': hour.get('snow', 0),
                'hour_snowdepth': hour.get('snowdepth', 0),
                'hour_windspeed': hour['windspeed'],
                'hour_visibility': hour['visibility'],
                'hour_cloudcover': hour['cloudcover'],
                'hour_conditions': hour['conditions'],
            }
            for hour in data[:12]
        ]
        return (hourly_forecast)
    else:
        return ('Error:', response.status_code, response.text)

if __name__ == '__main__':
    data = get_prediction_data_for_12_hours()
    print(data)