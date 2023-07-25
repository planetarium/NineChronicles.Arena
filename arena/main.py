import os

import uvicorn
from fastapi import FastAPI
from mangum import Mangum

from arena import settings

__VERSION__ = "0.0.1"

stage = os.environ.get("STAGE", "local")

app = FastAPI(
    title="Nine Chronicles Arena Service",
    description="",
    version=__VERSION__,
    root_path=f"/{stage}" if stage != "local" else "",
    debug=settings.DEBUG
)


@app.get("/ping", tags=["Default"])
def ping():
    """
    This API is for test connectivity.

    This API always returns string "pong" with HTTP status code 200
    """
    return "pong"


handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=settings.DEBUG)
