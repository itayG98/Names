import json
import sys
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

sys.path.append('C:\\temp\\Names\\NamesModel')
from NamesModel.PredictingApi import *


async def get_api():
    return await PredictingApi.init_class()


router = APIRouter(
    prefix="/Names",
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get() -> JSONResponse:
    is_ready = await get_api()
    if is_ready:
        return JSONResponse(content={"is_ready": PredictingApi.is_ready})


@router.get("/info")
async def get():
    is_ready = await get_api()
    if is_ready:
        return json.dumps(
            {"info": "This Api developed by Itay Getahun and the AI model is ready :" + str(PredictingApi.is_ready)})


@router.get("/name_count")
async def get_name_count(name: str, sheet_name: str, year: Optional[int] = PredictingApi.last_year) -> int:
    is_ready = await get_api()
    if is_ready:
        file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
        data = pd.read_excel(file_path, index_col=0)
        return data[name][year]
    return 0


@router.get("/top_names")
def get_top_names(sheet_name: str, year: Optional[int] = PredictingApi.last_year, startwith: str = "",
                  count: int = 25) -> list[str] | None:
    if PredictingApi.is_ready:
        file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
        data = pd.read_excel(file_path, index_col=0)
        row = data.loc[year]
        filtered_row = row[row.index.str.startswith(startwith)]
        return filtered_row.nlargest(count)
    return None


@router.get("/dataframe")
def get_df(sheet_name: str) -> Any | None:
    file_path = "Assets/Predicted_Names_" + sheet_name + ".xlsx"
    data = pd.read_excel(file_path, index_col=0)
    if data:
        return data
    return None

# http://127.0.0.1:5002/Names/top_names?sheet_name=Jew_male
