import csv
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd

def start_hour(row):
    time=row[5]
    timeline = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    t=timeline.replace(second=0, minute=0)
    row.append(t)
    return row

def end_hour(row):
    time=row[6]
    timeline = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    hour=timeline.hour
    if hour==23:
        t = timeline.replace(second=0, minute=0, hour=0) + timedelta(days=1)
    else:
        t= timeline.replace(second=0, minute=0, hour=hour+1)
    row.append(t)
    return row

def date_converter(row):
    time=row[5]
    timeline = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    row.append(timeline.date())
    return row


def next_day(row):
    date = row[0]
    dateline = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
    row[0]=str(dateline.date())
    return row

def add_ukraine(row):
    city=row[3]
    city_with_ukraine= city + ", Україна"
    row[3]=city_with_ukraine
    return row

def add_city_for_merge(row):
    region_id={'1': 'Chernivtsi,Ukraine',
               '2': 'Lutsk,Ukraine',
               '3': 'Vinnytsia,Ukraine',
               '4': 'Dnipro,Ukraine',
               '5': 'Donetsk,Ukraine',
               '6': "Zhytomyr,Ukraine",
               '7': 'Uzhgorod,Ukraine',
               '8': "Zaporozhye,Ukraine",
               '9': "Kyiv,Ukraine",
               '10': "Kropyvnytskyi,Ukraine",
               '12': "Lviv,Ukraine",
               '13':"Mykolaiv,Ukraine",
               '14': "Odesa,Ukraine",
               '15':"Poltava,Ukraine",
               '16':"Rivne,Ukraine",
               '17':"Sumy,Ukraine",
               '18': "Ternopil,Ukraine",
               '19':'Kharkiv,Ukraine',
               '20':"Kherson,Ukraine",
               '21':"Khmelnytskyi,Ukraine",
               '22':'Cherkasy,Ukraine',
               '23':'Chernihiv,Ukraine',
               '24':'Ivano-Frankivsk,Ukraine'}
    id=row[1]
    row.append(region_id[id])
    return row

with open('enriched_alarms.csv', encoding="utf-8") as file_obj:
    reader_obj = csv.reader(file_obj, delimiter=';')
    row0=next(reader_obj, None)
    row0.extend(["date_of_alarm", "start_hour_epoch", "end_hour_epoch", "city_for_merge"])
    data=list(reader_obj)

with open('enriched_alarms1.csv', 'w', newline='', encoding='UTF8') as f:
    writer=csv.writer(f, delimiter=';')
    writer.writerow(row0)
    new_data=[]
    data_with_dates=list(map(date_converter, data))
    data_with_start_hour=list(map(start_hour, data_with_dates))
    data_with_end_hour=list(map(end_hour, data_with_start_hour))
    data_with_city_for_merge=list(map(add_city_for_merge, data_with_end_hour))

    for row in data_with_end_hour:
        writer.writerow(row)

df_events=pd.read_csv('enriched_alarms1.csv', delimiter=';')
events_dict=df_events.to_dict('records')
events_by_hour=[]

for event in events_dict:
    for d in pd.date_range(start=event["start_hour_epoch"], end=event["end_hour_epoch"], freq='1H'):
        et = event.copy()
        et["hour_level_event_time"] = int(d.timestamp())
        events_by_hour.append(et)
df_events_v3 = pd.DataFrame.from_dict(events_by_hour)

with open('2022-02-24 - 2023-03-24-isw.csv', encoding="utf-8") as file_obj:
    reader_obj = csv.reader(file_obj, delimiter=',')
    row0=next(reader_obj, None)
    row0[0]="date_for_merge"
    data=list(reader_obj)

with open('isw_for_merge.csv', 'w', newline='', encoding='UTF8') as f:
    writer=csv.writer(f, delimiter=';')
    writer.writerow(row0)
    data_for_merge=list(map(next_day, data))
    for row in data_for_merge:
        writer.writerow(row)

df_events_v3 = pd.DataFrame.from_dict(events_by_hour)
df_weather=pd.read_csv('all_weather_by_hour.csv')

weather_exclude = [
"day_feelslikemax",
"day_feelslikemin",
"day_sunriseEpoch",
"day_sunsetEpoch",
"day_description",
"city_latitude",
"city_longitude",
"city_timezone",
"city_tzoffset",
"day_feelslike",
"day_precipprob",
"day_snow",
"day_snowdepth",
"day_windgust",
"day_windspeed",
"day_winddir",
"day_pressure",
"day_cloudcover",
"day_visibility",
"day_severerisk",
"day_conditions",
"day_icon",
"day_source",
"day_preciptype",
"day_stations",
"hour_icon",
"hour_source",
"hour_stations",
"hour_feelslike"
]

df_news=pd.read_csv('isw_for_merge.csv', delimiter=';')
df_weather_v2 = df_weather.drop(weather_exclude, axis=1)

df_alarms_news=pd.merge(df_events_v3, df_news, left_on='date_of_alarm', right_on='date_for_merge')
df_alarms_weather=pd.merge(df_events_v3, df_weather_v2,  left_on=['hour_level_event_time', 'city_for_merge'], right_on=['hour_datetimeEpoch', 'city_address'])
df_alarms_weather_news=pd.merge(df_alarms_weather, df_news, left_on='date_of_alarm', right_on='date_for_merge')

df_alarms_news.to_csv('final_alarms_news.csv', sep=';')
df_alarms_weather.to_csv('final_alarms_weather.csv', sep=';')
df_alarms_weather_news.to_csv('final_alarms_weather_news.csv', sep=';')
