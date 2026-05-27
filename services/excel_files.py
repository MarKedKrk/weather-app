import pandas as pd
from config import Config
import os

def save_to_excel(data):
    PATH = Config.EXCEL_PATH

    try:
        new_df = pd.DataFrame(data)
        if os.path.exists(PATH):
            current = pd.read_excel(PATH)
            concat_data = pd.concat(
                [current, new_df],
                ignore_index=True,
            )
            concat_data.to_excel(PATH, index=False)
        else:
            new_df.to_excel(PATH, index=False)

    except Exception as e:
        print(e)

def read_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        return df

    except Exception as e:
        print(e)