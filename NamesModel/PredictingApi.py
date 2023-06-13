import json
import os

import pandas as pd
from dotenv import load_dotenv, find_dotenv
from ModelCreator import init, load_data
from asyncio import Task


class PredictingApi:
    load_dotenv(find_dotenv())
    predicting = "Assets/" + os.environ.get("PREDICTING_YEARS")
    last_year = "Assets/" + os.environ.get("YEAR_ENDED")

    def __init__(self, task: Task):
        # Build the model
        init()
        sheets, path = load_data()
        for sheet in sheets:
            sheet["predicted_CSV"] = "Assets/Predicted_Names_" + sheet["englishName"] + ".xlsx"

    def get_name_count(self, name: str, sheet_name: str, year: int = last_year + 1) -> int:
        file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
        data = pd.read_excel(file_path)
        return data[name][year]

    def get_top_names(self, sheet_name: str, year: int = last_year + 1,count : int = 25) -> int:
        file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
        data = pd.read_excel(file_path)
        relevant_year = data.iloc[year]

