import pandas as pd

FILE_PATH = 'data/weather_alarms_news.csv'
RESULT_FILE_PATH = 'data/clear_full_dataset.csv'
if __name__ == "__main__":
    df = pd.read_csv(FILE_PATH, sep=';')
    # we assume to predict alarm in region for some hour, 
    # so include only data that can be useful for this
    df = df[[
        "region_title", 
        "all_region", 
        "alarms_in_other_regions", 
        "regions_in_fire", 
        "quantity_regions_in_fire",
        "alarms_in_region_for_last_24H",
        "duration", 
        "Short/Long",
        "start_hour_epoch",
        "hour_temp",
        "hour_humidity",
        "hour_snow",
        "hour_windspeed",
        "hour_visibility",
        "hour_cloudcover",
        "hour_conditions",
        "news",
        "is_alarm"]]
    
    df.to_csv(RESULT_FILE_PATH, sep=";")