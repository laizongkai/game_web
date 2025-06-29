from typing import Union
from fastapi import FastAPI
from .routers import product, selling
from .sql.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.getLogger().handlers = []
logging.basicConfig(
    level = logging.INFO,
    format = "[%(levelname).4s] [%(asctime)s] - %(message)s",
    handlers = [logging.StreamHandler()]
) 

app = FastAPI()

app.include_router(product.router)
app.include_router(selling.router)

origins=[
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://0.0.0.0:5173",
    "http://0.0.0.0:8080",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "App"}


@app.on_event("startup")
def configure():
    logging.info("Start the app.")
    Base.metadata.create_all(bind = engine)
