import fnmatch
import os
import ast
import csv
import datetime
import time
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict


dates = ['2022-02-25', '2022-03-24', '2022-04-24', '2022-05-24', '2022-06-24', '2022-07-24', '2022-08-24',
       '2022-09-24', '2022-10-24', '2022-11-25', '2022-12-24', '2023-01-24', '2023-02-24', '2023-03-24']

dates_weather = ['2022-02-25', '2022-03-24', '2022-04-24', '2022-05-24', '2022-06-24', '2022-07-24', '2022-08-24',
       '2022-09-24', '2022-10-24', '2022-11-25', '2022-12-24', '2023-01-20']


def file_search_by_pattern(pattern, dates):
    for file in os.listdir():
        if fnmatch.fnmatch(file, pattern):
            dict = {}
            with open(file) as file_obj:
                reader_obj = csv.reader(file_obj)
                for row in reader_obj:
                    if row[0] in dates:
                        dict[row[0]] = ast.literal_eval(row[1])
    return dict


date_news=file_search_by_pattern('*isw.csv', dates)
first_n_values = 20
for date in date_news.keys():
    data = date_news[date]
    names = list(data.keys())
    values = list(data.values())
    plt.scatter(names[:first_n_values], values[:first_n_values])
    plt.xlabel('Words from vectored news', fontsize=14, fontweight='bold')
    plt.ylabel('Vector values', fontsize=14, fontweight='bold')
    for i in names[:first_n_values]:
        plt.text(i, data[i], str(data[i]), fontsize=8)
    plt.title(date, fontsize=14, fontweight='bold')
    plt.show()
    plt.close()


def visibility_for_dates(city, dates):
    with open('all_weather_by_hour.csv', encoding="utf-8") as file_obj:
        reader_obj = csv.reader(file_obj)
        visibility=[]
        for row in reader_obj:
            if row[3]==city+',Ukraine' and row[6] in dates:
                visibility.append(float(row[26]))
    return visibility[::24]


def cloud_cover_for_dates(city, dates):
    with open('all_weather_by_hour.csv', encoding="utf-8") as file_obj:
        reader_obj = csv.reader(file_obj)
        cloud_cover=[]
        for row in reader_obj:
            if row[3]==city+',Ukraine' and row[6] in dates:
                cloud_cover.append(float(row[25]))
    return cloud_cover[::24]

cities=['Kharkiv', 'Kyiv']

for city in cities:
    names = dates_weather
    values = visibility_for_dates(city, dates_weather)
    plt.bar(names, values)
    plt.xlabel('Dates', fontsize=14, fontweight='bold')
    plt.ylabel('Visibility', fontsize=14, fontweight='bold')
    plt.title('Visibility ' + city, fontsize=14, fontweight='bold')
    plt.show()
    plt.close()

for city in cities:
    names = dates_weather
    values = cloud_cover_for_dates(city, dates_weather)
    plt.bar(names, values)
    plt.xlabel('Dates', fontsize=14, fontweight='bold')
    plt.ylabel('Cloud Cover', fontsize=14, fontweight='bold')
    plt.title('Cloud Cover ' + city, fontsize=14, fontweight='bold')
    plt.show()
    plt.close()

region_id={'Chernivtsi': '1','Lutsk': '2', 'Vinnytsia': '3', 'Dnipro': '4', 'Donets': '5',
           'Zhytomir': '6', 'Uzhgorod': '7', 'Zaporozhye': '8', 'Kyiv': '9',
           'Kropyvnytskyi': '10', 'Lviv': '12', 'Mykolaiv': '13', 'Odesa': '14',
           'Poltava': '15', 'Rivne': '16', 'Sumy': '17', 'Ternopil': '18', 'Kharkiv': '19',
           'Kherson': '20', 'Khmelnytskyi': '21', 'Cherkasy': '22', 'Chernihiv':'23',
           'Ivano-Frankivsk': '24'}

def long_alarm(city, dates):
    with open('alarms.csv', encoding="utf-8") as file_obj:
        reader_obj = csv.reader(file_obj,  delimiter=';')
        next(reader_obj, None)
        dict = defaultdict(int)
        for row in reader_obj:
            if row[1]==region_id[city] and row[5].split(" ")[0] in dates:
                time_alarm = round(((datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')-
                                     datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')).total_seconds())/3600, 2)
                dict[row[5].split(" ")[0]] += float(time_alarm)
    return dict

cities=['Kharkiv', 'Kyiv', 'Kherson']
for city in cities:
    names = long_alarm(city, dates_weather).keys()
    values = long_alarm(city, dates_weather).values()
    plt.bar(names, values)
    plt.xlabel('Dates', fontsize=14, fontweight='bold')
    plt.ylabel('Alarms long, hours', fontsize=14, fontweight='bold')
    plt.title('Alarms long ' + city+ ', hours', fontsize=14, fontweight='bold')
    for i in names:
        plt.text(i, long_alarm(city, dates_weather)[i], str(round(long_alarm(city, dates_weather)[i], 2)), fontsize=12, fontweight='bold' )
    plt.show()
    plt.close()