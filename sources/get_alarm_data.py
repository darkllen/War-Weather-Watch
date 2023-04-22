import requests
import csv
import time


region_id_alarms= {'Chernivtsi': '26','Lutsk': '8', 'Vinnytsia': '4', 'Dnipro': '9', 'Donetsk': '28',
           'Zhytomyr': '10', 'Uzhgorod': '11', 'Zaporozhye': '12', 'Kyiv': '14',
           'Kropyvnytskyi': '15', 'Lviv': '27', 'Mykolaiv': '17', 'Odesa': '18',
           'Poltava': '19', 'Rivne': '5', 'Sumy': '20', 'Ternopil': '21', 'Kharkiv': '22',
           'Kherson': '23', 'Khmelnytskyi': '3', 'Cherkasy': '24', 'Chernihiv':'25',
           'Ivano-Frankivsk': '13'}

region_id_weather = {'Chernivtsi': '1', 'Lutsk': '2', 'Vinnytsia': '3', 'Dnipro': '4', 'Donetsk': '5',
            'Zhytomir': '6', 'Uzhgorod': '7', 'Zaporozhye': '8', 'Kyiv': '9',
            'Kropyvnytskyi': '10', 'Lviv': '12', 'Mykolaiv': '13', 'Odesa': '14',
            'Poltava': '15', 'Rivne': '16', 'Sumy': '17', 'Ternopil': '18', 'Kharkiv': '19',
            'Kherson': '20', 'Khmelnytskyi': '21', 'Cherkasy': '22', 'Chernihiv':'23',
            'Ivano-Frankivsk': '24'}

def last_alarms(region):
    url = 'https://api.ukrainealarm.com/api/v3/alerts/regionHistory'
    params = {'regionId': region_id_alarms[region]}
    headers = {
        'accept': 'application/json',
        'Authorization': f'{API_KEY}'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0]['alarms']
    else:
        return response.status_code
        
rows=[]
for region in region_id_alarms:
    for i in last_alarms(region):
        i['regionId']=region_id_weather[region]
        i['regionCity']=region
        i['startDate']=i['startDate'].replace('T', ' ')
        i['endDate'] = i['endDate'].replace('T', ' ')
        rows.append(i)

row0=["id", "region_id", "region_title", "region_city", "all_region", "start", "end"]

with open(f'train_file_{str(int(time.time()))}.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(row0)
    counter=1
    for dict in rows:
        region_id=dict['regionId']
        region_title=dict['regionCity']
        region_city=dict['regionCity']
        start = dict['startDate']
        end = dict['endDate']
        writer.writerow([counter, region_id, region_title, region_city, 0, start, end])
        counter+=1
