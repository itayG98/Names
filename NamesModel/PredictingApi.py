import json
import os
from dotenv import load_dotenv, find_dotenv
from ModelCreator import init, load_data
from asyncio import Task


class PredictingApi:
    def __init__(self, task: Task):
        # Build the model
        init()
        sheets, path = load_data()
        for sheet in sheets:
            sheet["predicted_CSV"] = "Assets/Predicted_Names_" + sheet["englishName"] + ".xlsx"
