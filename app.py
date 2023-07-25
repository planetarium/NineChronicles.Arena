#!/usr/bin/env python3
import logging
import os

import aws_cdk as cdk
from dotenv import dotenv_values

from arena.arena_cdk_stack import ArenaStack
from common import Config
from common.shared_stack import SharedStack

stage = os.environ.get("STAGE", "development")

if os.path.exists(f".env.{stage}"):
    env_values = dotenv_values(f".env.{stage}")
    if stage != env_values["STAGE"]:
        logging.error(f"Provided stage {stage} is not identical with STAGE in env: {env_values['STAGE']}")
        exit(1)
else:
    env_values = os.environ

config = Config(**{k.lower(): v for k, v in env_values.items()})

app = cdk.App()

shared = SharedStack(
    app, f"{config.stage}-9c-arena-SharedStack",
    env=cdk.Environment(
        account=config.account_id, region=config.region_name,
    ),
    config=config,
)

ArenaStack(
    app, f"{config.stage}-9c-arena-APIStack",
    env=cdk.Environment(
        account=config.account_id, region=config.region_name,
    ),
    config=config,
    shared_stack=shared,
)

app.synth()
