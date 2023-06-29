from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from Backend.routers.names_router import router


app = FastAPI(title="Israeli baby", description="This is a web API using FastApi for Israeli baby application")
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", status_code=200)
def read_root():
    return RedirectResponse("/info")


@app.get("/info", status_code=301)
def read_root():
    return dict(msg='This API developed by ItayG98')



