import csv
from datetime import datetime
from datetime import timedelta

with open('alarms.csv', encoding="utf-8") as file_obj:
    reader_obj = csv.reader(file_obj, delimiter=';')
    row0=next(reader_obj, None)
    row0.pop()
    row0.extend(["alarms_in_other_regions", 'regions_in_fire', "quantity_regions_in_fire","alarms_in_region_for_last_24H", "duration", "Short/Long"])
    data=list(reader_obj)

def converter(time):
    return datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

with open('enriched_alarms.csv', 'w', newline='', encoding='UTF8') as f:
    writer=csv.writer(f, delimiter=';')
    writer.writerow(row0)
    new_data=[]
    for rowx in data:
        rowx.pop()
        same_day=[]
        tested_start=converter(rowx[5])
        tested_end = converter(rowx[6])
        same_day=list(filter(lambda x: rowx[5].split(' ')[0]==x[5].split(' ')[0] and  rowx[1]!=x[1], data))
        non_same_time_alarm=list(filter(lambda x: converter(x[6]) < tested_start or converter(x[5]) > tested_end,same_day))
        same_alarms=[]
        for i in same_day:
            if i not in non_same_time_alarm:
                same_alarms.append(i)

        regions_in_fire = list(set(map(lambda x: x[2], same_alarms)))
        str_regions_in_fire=" ".join(regions_in_fire)
        last24h=list(filter(lambda x: x[1]==rowx[1] and tested_start-timedelta(hours=24)<=converter(x[6])<=tested_start, data))
        seconds=int((tested_end-tested_start).total_seconds())
        duration=str(timedelta(seconds=seconds))
        long=""
        if seconds>3600*3:
            long="Long"
        else:long="Short"
        rowx.extend([len(same_alarms), str_regions_in_fire, len(regions_in_fire), len(last24h), duration, long])
        writer.writerow(rowx)