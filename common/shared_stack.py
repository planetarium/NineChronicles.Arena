from dataclasses import dataclass
from dataclasses import dataclass
from typing import Dict

from aws_cdk import (
    Stack,
    aws_ec2 as _ec2,
)
from constructs import Construct

from common import Config


@dataclass
class ResourceDict:
    vpc_id: str


RESOURCE_DICT: Dict[str, ResourceDict] = {
    "development": ResourceDict(
        vpc_id="vpc-0cf2339a10213911d",  # Test VPC in AWS Dev Account - apne2 region
    ),
    "internal": ResourceDict(
        vpc_id="vpc-08ee9f2dbd1c97ac6",  # Internal VPC
    ),
    "mainnet": ResourceDict(
        vpc_id="vpc-01a0ef2aa2c41bb26",  # Main VPC
    ),
}


class SharedStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        config: Config = kwargs.pop("config")
        resource_data = RESOURCE_DICT.get(config.stage, None)
        if resource_data is None:
            raise KeyError(f"{config.stage} is not valid stage. Please select one of {list(RESOURCE_DICT.keys())}")
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        self.vpc = _ec2.Vpc.from_lookup(self, f"{config.stage}-9c-iap-vpc", vpc_id=resource_data.vpc_id)
