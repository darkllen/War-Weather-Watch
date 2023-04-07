import pandas as pd

FILE_PATH = 'data/weather_alarms_news_vectorized.csv'
RESULT_FILE_PATH = 'data/clear_full_dataset.csv'
if __name__ == "__main__":
    df = pd.read_csv(FILE_PATH, sep=';')
    # we assume to predict alarm in region for some hour, 
    # so include only data that can be useful for this
    df = df.drop(columns=[
        'Unnamed: 0',
        'city_resolvedAddress', 
        'city_address',
        'day_datetime',
        'day_tempmax',
        'day_tempmin',
        'day_temp',
        'day_dew',
        'day_humidity',
        'day_precip',
        'day_precipcover',
        'day_solarradiation',
        'day_solarenergy',
        'day_uvindex',
        'day_sunrise',
        'day_sunset',
        'day_moonphase',
        'hour_datetime',
        'hour_datetimeEpoch',
        'hour_dew',
        'hour_precip',
        'hour_precipprob',
        'depth',
        'hour_preciptype',
        'hour_windgust',
        'hour_winddir',
        'hour_pressure',
        'hour_solarradiation',
        'hour_solarenergy',
        'hour_uvindex',
        'hour_severerisk',
        'id',
        'region_title',
        'region_city',
        'start_x',
        'end_x',
        'date_of_alarm',
        'start_hour_epoch',
        'end_hour_epoch',
        'date_of_alarm.1',
        'start_hour_epoch.1',
        'end_hour_epoch.1',
        'city_for_merge', 
        'hour_level_event_time',
        'date_for_merge',
    ])
    
    df.to_csv(RESULT_FILE_PATH, sep=";")