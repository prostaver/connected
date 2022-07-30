import configparser
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.api import router

import uvicorn

app = FastAPI()

origins = ["http://locahost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

# for gunicorn server
# run in console
# gunicorn main:app --workers 4 -- worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
# where main = module name, app = fastapi() name, workers = (no. of cpu cores * 2) + 1, and bind = ipaddress:port
if __name__ == '__main__':
    config = configparser.ConfigParser()

    config.read(os.path.dirname(os.path.abspath(__file__))+"/config/config.ini")
    config.sections()

    if config['DEFAULT']['ENVIRONMENT'] == "development":
        uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)
    print("running")
