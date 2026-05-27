from services.openweather_api import get_weather
import time

while True:
    weather = get_weather()
    print(weather)
    print("Udało się pobrać dane!!!")
    time.sleep(10)
