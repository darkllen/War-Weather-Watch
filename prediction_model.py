import csv
import time
import ast
import requests
import datetime
from datetime import date, timedelta


with open('test.csv', encoding="utf-8") as file_obj:
    reader_obj = csv.reader(file_obj, delimiter=';')
    row0=next(reader_obj, None)
    rowdict=row0[19::]


today = date.today()
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")

with open(f'2022-02-24 - {yesterday_str}-isw.csv', encoding="utf-8") as file_obj:
    reader_obj = csv.reader(file_obj, delimiter=';')
    data=list(reader_obj)[-1][0][12:-1:]
    current_dict= ast.literal_eval(data)
    dict_news= {}
    for i in current_dict.keys():
        if i in rowdict:
            dict_news[i]=current_dict[i]

name_file=f'predict-{str(int(time.time()))}.csv'

region_id={'Chernivtsi': '1','Lutsk': '2', 'Vinnytsia': '3', 'Dnipro': '4', 'Donets': '5',
           'Zhytomir': '6', 'Uzhgorod': '7', 'Zaporozhye': '8', 'Kyiv': '9',
           'Kropyvnytskyi': '10', 'Lviv': '12', 'Mykolaiv': '13', 'Odesa': '14',
           'Poltava': '15', 'Rivne': '16', 'Sumy': '17', 'Ternopil': '18', 'Kharkiv': '19',
           'Kherson': '20', 'Khmelnytskyi': '21', 'Cherkasy': '22', 'Chernihiv':'23',
           'Ivano-Frankivsk': '24'}

now = datetime.datetime.now()
rounded_hour = (now.replace(second=0, microsecond=0, minute=0, hour=now.hour)
                 + datetime.timedelta(hours=1))
print(rounded_hour)

BASE_URL='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
API_KEY=''

def get_weather(city = 'Kyiv'):
    url = f'{BASE_URL}/{city}'
    params = {
        'unitGroup': 'metric',
        'key': f'{API_KEY}',
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

with open(name_file, 'w', newline='', encoding='UTF8') as f:
    writer=csv.writer(f, delimiter=';')
    writer.writerow(row0)
    for region in region_id:
        new_data=[None]*len(row0)
        forecast=get_weather(region+',Ukraine')
        index = row0.index("region_id")
        new_data[index] = region_id[region]
        for i in dict_news.keys():
            index = row0.index(i)
            new_data[index] = dict_news[i]
        for hour in forecast:
            for weather_value in hour.keys():
                index = row0.index(weather_value)
                new_data[index]=hour[weather_value]
            writer.writerow(new_data)
print(f'File {name_file} was created successful!')
