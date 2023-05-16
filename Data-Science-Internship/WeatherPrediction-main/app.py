from flask import Flask, url_for, render_template, request
import requests 
import json

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():

    if request.method == "POST":
        city = request.form['city']
        country = request.form['country']
        api_key = '8539e5a699e66777e34d82f37d615760'


        weather_url = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city},{country}&units = imperial')


        weather_data = weather_url.json()
        weather_desc = weather_data['weather'][0]['description']
        temp = round(weather_data['main']['temp'])
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']


        return render_template('result.html',weather_desc = weather_desc, temp = temp, temp_min = temp_min, temp_max = temp_max, humidity = humidity, wind_speed = wind_speed, city = city )

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug = True)