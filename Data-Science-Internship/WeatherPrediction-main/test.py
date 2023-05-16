import requests
import json

city = 'Indianapolis'
country = 'US'

api_key = "###"

weather_url = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid = {api_key}&q = {city}, {country}&units = imperial')

weather_data = weather_url.json()

weather_desc = weather_data['weather'][0]['description']

temp = round(weather_data['main']['temp'])

temp_min = weather_data['main']['temp_min']

temp_max = weather_data['main']['temp_max']

humidity = weather_data['main']['humidity']

wind_speed = weather_data['wind']['speed']