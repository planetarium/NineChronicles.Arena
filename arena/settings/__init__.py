import logging
import os

from starlette.config import Config

from common.utils.aws import fetch_secrets

stage = os.environ.get("STAGE", "local")
db_password = None

if not stage:
    logging.error("Config file not found")
    raise FileNotFoundError(f"No config file for environment [{stage}]")

if os.path.exists(os.path.join("arena", "settings", f"{stage}.py")):
    env_module = __import__(f"arena.settings.{stage}", fromlist=["arena.settings"])
    envs = {k: v for k, v in env_module.__dict__.items() if k.upper() == k}
    config = Config(environ=envs)
else:
    config = Config(environ=os.environ)
    db_password = fetch_secrets(os.environ.get("REGION_NAME"), os.environ.get("SECRET_ARN"))["password"]

DEBUG = config("DEBUG", cast=bool, default=False)
LOG_LEVEL = logging.getLevelName(config("LOG_LEVEL", default="INFO"))

DB_URI = config("DB_URI")
if db_password is not None:
    DB_URI = DB_URI.replace("[DB_PASSWORD]", db_password)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)

REGION_NAME = config("REGION_NAME")
