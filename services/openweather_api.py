import requests
from datetime import datetime
from config import Config
from utils.tools import to_celcious
from utils.tools import to_kmh

API_KEY = Config.API_KEY
API_QUERY = Config.API_QUERY

def get_weather():
    API_URL  = f"https://api.openweathermap.org/data/2.5/weather?q={API_QUERY}&appid={API_KEY}"


    try:
        response = requests.get(API_URL)
        data = response.json()

        weather = {
            "name" : data.get("name"),
            "temperature" : to_celcious(data.get("main").get("temp")),
            "feels_like" : to_celcious(data.get("main").get("feels_like")),
            "wind_speed" : to_kmh(data.get("wind").get("speed")),
            "pressure" : data.get("main").get("pressure"),
            "clouds" : data.get("clouds").get("all"),
            "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sunrise" : datetime.fromtimestamp(data.get("sys").get("sunrise")).strftime("%Y-%m-%d %H:%M:%S"),
            "sunset" : datetime.fromtimestamp(data.get("sys").get("sunset")).strftime("%Y-%m-%d %H:%M:%S")
        }

        return weather

    except Exception as e:
        print(e)