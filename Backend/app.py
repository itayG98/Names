import NamesModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Chat API", description="This is a Chat service web API using FastApi MongDB Beanie and Pydntic "
                                            "The "
                                            "server use Beanie  Document for chat between two users and Pydantic "
                                            "BaseModel for a single message schema")

##app.include_router(ModelRouter)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event('startup')
async def connect():
    pass


@app.get("/", status_code=200)
def read_root():
    return RedirectResponse("/info")


@app.get("/info", status_code=301)
def read_root():
    return dict(msg='This API developed by ItayG98')


