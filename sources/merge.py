import pandas as pd
import numpy as np

DATA_FOLDER = 'data'

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

df_events=pd.read_csv(f'{DATA_FOLDER}/enriched_alarms1.csv', delimiter=';')
events_dict=df_events.to_dict('records')
events_by_hour=[]
for event in events_dict:
    for d in pd.date_range(start=event["start_hour_epoch"], end=event["end_hour_epoch"], freq='1H'):
        et = event.copy()
        et["hour_level_event_time"] = int(d.timestamp())
        events_by_hour.append(et)
df_events_v3 = pd.DataFrame.from_dict(events_by_hour)

df_news=pd.read_csv(f'{DATA_FOLDER}/isw_for_merge.csv', delimiter=';')

df_weather=pd.read_csv(f'{DATA_FOLDER}/all_weather_by_hour_v2.csv')
df_weather_v2 = df_weather.drop(weather_exclude, axis=1)


df_weather_alarms=pd.merge(df_weather_v2, df_events_v3, how='left', left_on=['hour_datetimeEpoch', 'city_address'], right_on=['start_hour_epoch', 'city_for_merge'])
df_weather_alarms['is_alarm']=np.where(df_weather_alarms['start'].isnull(), 0, 1)

df_weather_alarms_news=pd.merge(df_weather_alarms, df_news, left_on='day_datetime', right_on='date_for_merge')
df_weather_alarms_news.to_csv(f'{DATA_FOLDER}/weather_alarms_news.csv', sep=';')
