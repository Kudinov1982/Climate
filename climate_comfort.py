import pandas as pd
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_comfort_index(temp, humidity, wind, rain, sun, 
                            opt_temp=22, opt_humidity=50, opt_wind=2, opt_rain=700, opt_sun=200):
    temp_score = max(0, 100 - abs(temp - opt_temp) * 3)
    humidity_score = max(0, 100 - abs(humidity - opt_humidity) * 1.5)
    wind_score = max(0, 100 - abs(wind - opt_wind) * 10)
    rain_score = max(0, 100 - (rain / 20))
    sun_score = min(100, (sun / 2))
    
    comfort_index = round((temp_score * 0.3 + humidity_score * 0.2 + wind_score * 0.15 + 
                           rain_score * 0.2 + sun_score * 0.15), 2)
    return comfort_index

# Генерация базы данных с климатическими данными
city_names = ["Москва", "Лондон", "Берлин", "Париж", "Мадрид", "Рим", "Пекин", "Нью-Йорк", "Торонто", "Сидней"]
additional_cities = [f"Город {i}" for i in range(1, 191)]
all_cities = city_names + additional_cities

city_data = pd.DataFrame({
    "Город": all_cities,
    "Температура": [random.uniform(-5, 30) for _ in all_cities],
    "Влажность": [random.randint(30, 90) for _ in all_cities],
    "Ветер": [random.uniform(1, 10) for _ in all_cities],
    "Осадки": [random.randint(200, 2000) for _ in all_cities],
    "Солнце": [random.randint(50, 300) for _ in all_cities]
})

@app.route('/')
def index():
    return render_template('index.html', cities=city_data["Город"].tolist())

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    city_info = city_data[city_data["Город"] == data['city']].iloc[0]
    index = calculate_comfort_index(city_info['Температура'], city_info['Влажность'], city_info['Ветер'], 
                                    city_info['Осадки'], city_info['Солнце'], 
                                    data['opt_temp'], data['opt_humidity'], data['opt_wind'], 
                                    data['opt_rain'], data['opt_sun'])
    return jsonify({"index": index})

if __name__ == '__main__':
    app.run(debug=True)
