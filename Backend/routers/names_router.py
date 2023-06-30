import json
import sys
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse

sys.path.append('C:\\temp\\Names\\NamesModel')
sys.path.append("C:\\temp\\Names\\NamesModel\\Assets")
from NamesModel.PredictingApi import *


async def get_api():
    is_ready = await PredictingApi.init_class()
    print("The model is ready: " + str(PredictingApi.is_ready))
    return is_ready


router = APIRouter(
    prefix="/Names",
    responses={404: {"description": "Not found"}},
)
router.on_startup.append(get_api)


@router.get("/")
async def get() -> JSONResponse:
    return JSONResponse(content={"is_ready": PredictingApi.is_ready})


@router.get("/info")
async def get() -> JSONResponse:
    return JSONResponse(content={"info": "This Api developed by Itay Getahun and the AI model is ready :" +
                                         str(PredictingApi.is_ready)})


@router.get("/name_count")
async def get_name_count(name: str, sheet_name: str, year: Optional[int] = PredictingApi.last_year) -> JSONResponse:
    count = -1
    if PredictingApi.is_ready:
        count = int(PredictingApi.get_name_count(name, sheet_name, year))
    return JSONResponse(content={f"{name}": name, "count": count})


@router.get("/top_names")
def get_top_names(sheet_name: str, year: Optional[int] = PredictingApi.last_year, startwith: str = "",
                  count: int = 25) -> JSONResponse:
    top_names = []
    if PredictingApi.is_ready:
        top_names = list(PredictingApi.get_top_names(sheet_name, year, startwith, count))
    return JSONResponse(content={"names": top_names, "year": year , "startwith" : startwith , count : count})


@router.get("/dataframe")
def get_df(sheet_name: str) -> JSONResponse:
    sheet = {}
    if PredictingApi.is_ready:
        sheet = PredictingApi.get_df(sheet_name).to_dict()
    return JSONResponse(content={"sheet": sheet})

# http://127.0.0.1:5001/Names/top_names?sheet_name=Jew_male
#http://127.0.0.1:5001/Names/name_count?name=%D7%A0%D7%99%D7%A8&sheet_name=Jew_male&year=2022
#http://127.0.0.1:5001/Names/dataframe?sheet_name=Jew_male
