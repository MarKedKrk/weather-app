from services.render_dashboard import render_dashboard
from services.excel_files import read_from_excel
from config import Config
import time

# while True:
    # weather = get_weather()
    # save_to_excel([weather])
    # print("Udało się pobrać dane!!!")
    # time.sleep(10)

# df = read_from_excel(Config.EXCEL_PATH)
# print(df)

#==============================
#         ZAJĘCIA 10.06
#==============================

render_dashboard("lisbon_weather_450.csv")