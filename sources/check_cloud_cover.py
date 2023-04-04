import csv
from datetime import datetime

def epoch_converter(dateline):
    timeline = datetime.strptime(dateline, '%Y-%m-%d')
    return timeline.timestamp()

with open('all_weather_by_hour_v2.csv', encoding="utf-8") as file_obj:
    reader_obj = csv.reader(file_obj, delimiter=',')
    row0=next(reader_obj, None)
    data=list(reader_obj)

def check_cloud_cover(start, end, data):
    weather_for_hours = list(
        filter(lambda x: epoch_converter(start) <= float(x[43]) <= epoch_converter(end), data))
    cloud_cover = list(map(lambda x: float(x[58]), weather_for_hours))
    average_cloud_cover = sum(cloud_cover) / len(cloud_cover)
    return round(average_cloud_cover, 2)
