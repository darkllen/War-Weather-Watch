import json
import requests
import datetime

API_KEY=''

def getweather(city='Kyiv', country='UA', hours=12):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    location=city+','+country
    date1=round(datetime.datetime.now().timestamp())
    date2=date1+hours*3600
    url=f'{base_url}/{location}/{date1}/{date2}/?key={API_KEY}'
    response = requests.request("GET", url)
    return json.loads(response.text)

