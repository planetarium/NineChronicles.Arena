import logging
import os

from starlette.config import Config

stage = os.environ.get("STAGE", "local")

if not stage:
    logging.error("Config file not found")
    raise FileNotFoundError(f"No config file for environment [{stage}]")

if os.path.exists(os.path.join("arena", "settings", f"{stage}.py")):
    env_module = __import__(f"arena.settings.{stage}", fromlist=["arena.settings"])
    envs = {k: v for k, v in env_module.__dict__.items() if k.upper() == k}
    config = Config(environ=envs)
else:
    config = Config(environ=os.environ)

DEBUG = config("DEBUG", cast=bool, default=False)
LOG_LEVEL = logging.getLevelName(config("LOG_LEVEL", default="INFO"))

REGION_NAME = config("REGION_NAME")
