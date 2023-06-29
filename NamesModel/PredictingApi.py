import os
from typing import Any
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from ModelCreator import init, load_data


class PredictingApi:
    load_dotenv(find_dotenv())
    predicting = "Assets/" + os.environ.get("PREDICTING_YEARS")
    last_year = "Assets/" + os.environ.get("YEAR_ENDED")
    is_ready = False

    @staticmethod
    def __init__():
        raise Exception("Static classes cannot have constructors.")

    @staticmethod
    async def init_class():
        # Build the model
        print("initiating PredictingApi")
        if not PredictingApi.is_ready:
            PredictingApi.is_ready = await init()
            sheets, path = load_data()
            for sheet in sheets:
                sheet["predicted_CSV"] = "Assets/Predicted_Names_" + sheet["englishName"] + ".xlsx"
        return PredictingApi.is_ready

    @staticmethod
    def get_name_count(name: str, sheet_name: str, year: int = last_year) -> Any | None:
        if PredictingApi.is_ready:
            file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
            data = pd.read_excel(file_path, index_col=0)
            return data[name][year]
        return None

    @staticmethod
    def get_top_names(sheet_name: str, year: int = last_year, startwith: str = "", count: int = 25) -> Any | None:
        if PredictingApi.is_ready:
            file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
            data = pd.read_excel(file_path, index_col=0)
            row = data.loc[year]
            filtered_row = row[row.index.str.startswith(startwith)]
            return filtered_row.nlargest(count)
        return None

    @staticmethod
    def get_df(sheet_name: str) -> pd.DataFrame | None:
        if PredictingApi.is_ready:
            file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
            return pd.read_excel(file_path, index_col=0)
        return None
