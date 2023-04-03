import os
import json
import requests
import datetime

API_KEY=os.getenv('WEATHER_API_KEY')

BASE_URL='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

SECONDS_IN_HOUR = 3600

# TODO: The possibility to pass the date1 has to be added.
def get_weather(city = 'Kyiv', country = 'UA', hours = 12):
    location = city + ',' + country
    date1 = round(datetime.datetime.now().timestamp())
    date2 = date1 + hours * SECONDS_IN_HOUR
    url = f'{BASE_URL}/{location}/{date1}/{date2}/?key={API_KEY}'
    response = requests.request("GET", url)
    return json.loads(response.text)
