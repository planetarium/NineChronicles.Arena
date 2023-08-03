import os

import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from arena import settings, api

__VERSION__ = "0.0.1"

from common import logger

stage = os.environ.get("STAGE", "local")

app = FastAPI(
    title="Nine Chronicles Arena Service",
    description="",
    version=__VERSION__,
    root_path=f"/{stage}" if stage != "local" else "",
    debug=settings.DEBUG
)


def handle_400(e):
    logger.error(e)
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=str(e))


@app.exception_handler(ValueError)
def handle_value_error(request: Request, e: ValueError):
    return handle_400(e)


@app.get("/ping", tags=["Default"])
def ping():
    """
    This API is for test connectivity.

    This API always returns string "pong" with HTTP status code 200
    """
    return "pong"


@app.get("/robots.txt", response_class=FileResponse, tags=["Default"], summary="Returns robots.txt")
def robots():
    """
    This API returns robots.txt
    """
    return "arena/robots.txt"


app.include_router(api.router)

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=settings.DEBUG)
