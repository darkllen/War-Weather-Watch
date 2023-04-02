import csv
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
import ast

with open('final_alarms_weather_news.csv', encoding="utf-8") as file_obj:
    reader_obj = csv.reader(file_obj, delimiter=';')
    row0=next(reader_obj, None)
    data=list(reader_obj)

datas=[]
for row in data:
    if row[14] not in datas:
        datas.append(row[14])
dict={}
for alarm_date in datas:
    dict[alarm_date]=len(list(filter(lambda x: x[14]==alarm_date, data)))
values=list(dict.values())
keys=list(dict.keys())
maximum_atack = max(values)
day_with_max_attack= keys[values.index(maximum_atack)]
one_of_max_attack=(list(filter(lambda x: x[14]==day_with_max_attack, data)))[0]
news=ast.literal_eval(one_of_max_attack[-1])

first_n_values = 20
names = list(news.keys())
values = list(news.values())
plt.scatter(names[:first_n_values], values[:first_n_values])
plt.xlabel('Words from vectored news', fontsize=14, fontweight='bold')
plt.ylabel('Vector values', fontsize=14, fontweight='bold')
for i in names[:first_n_values]:
    plt.text(i, news[i]+0.003, str(news[i]), fontsize=8)
plt.title("Vector-news before the day with maximum of Alarms, 2022-03-14", fontsize=14, fontweight='bold')
plt.autoscale()
plt.show()
plt.close()

def share_alarms_hour_by_cloudcover(data, cloudcover):
    if cloudcover==100:
        er=1
    else:
        er = 0
    filtered_hours=list(filter(lambda x: cloudcover-10<=float(x[51])<=cloudcover+er, data))
    return round(len(filtered_hours)/len(data)*100, 2)

def share_alarms_hour_by_cloudcover_and_city(data, cloudcover, city):
    if cloudcover==100:
        er=1
    else:er=0
    filtered_hours=list(filter(lambda x: cloudcover-10<=float(x[51])<=cloudcover+er and x[17]==city+',Ukraine', data))
    filtered_by_region=list(filter(lambda x: x[17]==city+',Ukraine', data))
    return round(len(filtered_hours)/len(filtered_by_region)*100, 2)

cities=['Kyiv', 'Kharkiv', 'Lviv']
cloud_cover=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def share_alarms_hour_by_cloudcover_and_month(data, cloudcover, month):
    if cloudcover==100:
        er=1
    else:er=0
    for x in data:
        c=datetime.strptime(x[6], '%Y-%m-%d %H:%M:%S').month
        f=1
    filtered_hours=list(filter(lambda x: cloudcover-10<=float(x[51])<=cloudcover+er and
                               datetime.strptime(x[6], '%Y-%m-%d %H:%M:%S').month==month, data))
    filtered_by_month = list(
        filter(lambda x: datetime.strptime(x[6], '%Y-%m-%d %H:%M:%S').month == month, data))
    return round(len(filtered_hours)/len(filtered_by_month)*100, 2)

names = cloud_cover
values=[]
labels=[]
for i in names:
    values.append(share_alarms_hour_by_cloudcover(data, i))
    labels.append(str(i-10)+'%-'+str(i)+'%')
plt.bar(names, values, width=5)
plt.xlabel('Cloud Cover, %', fontsize=14, fontweight='bold')
plt.ylabel('Share in common amount of Alarm Hours, %', fontsize=14, fontweight='bold')
plt.title('Share of alarm hours for different cloud cover', fontsize=14, fontweight='bold')
plt.xticks(names, labels)
plt.autoscale()
for i in names:
    plt.text(i - 2, share_alarms_hour_by_cloudcover(data, i),
             str(round(share_alarms_hour_by_cloudcover(data, i), 2)) + '%',
             fontsize=12, fontweight='bold')
plt.show()
plt.close()

for city in cities:
    names = cloud_cover
    values = []
    labels = []
    for i in names:
        values.append(share_alarms_hour_by_cloudcover_and_city(data, i, city))
        labels.append(str(i - 10) + '%-' + str(i) + '%')
    plt.bar(names, values, width=5)
    plt.xlabel('Cloud Cover, %', fontsize=14, fontweight='bold')
    plt.ylabel('Share in common amount of Alarm Hours, %', fontsize=14, fontweight='bold')
    plt.title('Share of alarm hours for different cloud cover for ' + city, fontsize=14, fontweight='bold')
    plt.xticks(names, labels)
    plt.autoscale()
    for i in names:
        plt.text(i - 2, share_alarms_hour_by_cloudcover_and_city(data, i, city),
                 str(round(share_alarms_hour_by_cloudcover_and_city(data, i, city), 2)) + '%',
                 fontsize=12, fontweight='bold')
    plt.show()
    plt.close()

month_alarm=[3, 6, 9, 12]
year={3:'March', 6: 'June', 9:'September', 12: 'December'}
for month in month_alarm:
    names = cloud_cover
    values = []
    labels = []
    for i in names:
        values.append(share_alarms_hour_by_cloudcover_and_month(data, i, month))
        labels.append(str(i - 10) + '%-' + str(i) + '%')
    plt.bar(names, values, width=5)
    plt.xlabel('Cloud Cover, %', fontsize=14, fontweight='bold')
    plt.ylabel('Share in common amount of Alarm Hours, %', fontsize=14, fontweight='bold')
    plt.title('Share of alarm hours for different cloud cover for ' + year[month], fontsize=14,
              fontweight='bold')
    plt.xticks(names, labels)
    plt.autoscale()
    for i in names:
        plt.text(i-2, share_alarms_hour_by_cloudcover_and_month(data, i, month), str(round(share_alarms_hour_by_cloudcover_and_month(data, i, month), 2))+'%', fontsize=12, fontweight='bold' )
    plt.show()
    plt.close()