from dataclasses import dataclass
from typing import Dict

from aws_cdk import (
    Stack, RemovalPolicy,
    aws_ec2 as _ec2,
    aws_rds as _rds,
    aws_lambda as _lambda,
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
        self.vpc = _ec2.Vpc.from_lookup(self, f"{config.stage}-9c-arena-vpc", vpc_id=resource_data.vpc_id)

        # RDS
        self.rds_security_group = _ec2.SecurityGroup(
            self, f"{config.stage}-9c-arena-rds-sg", vpc=self.vpc, allow_all_outbound=True
        )
        self.rds_security_group.add_ingress_rule(
            peer=_ec2.Peer.ipv4("0.0.0.0/0"),
            connection=_ec2.Port.tcp(5432),
            description="Allow PSQL from outside",
        )
        self.rds_security_group.add_ingress_rule(
            peer=self.rds_security_group,
            connection=_ec2.Port.tcp(5432),
            description="Allow PSQL from outside",
        )
        self.credentials = _rds.Credentials.from_username("arena")
        self.rds = _rds.DatabaseInstance(
            self, f"{config.stage}-9c-arena-rds",
            instance_identifier=f"{config.stage}-9c-arena-rds",
            engine=_rds.DatabaseInstanceEngine.postgres(version=_rds.PostgresEngineVersion.VER_15_2),
            vpc=self.vpc,
            vpc_subnets=_ec2.SubnetSelection(),
            database_name="arena",
            credentials=self.credentials,
            instance_type=_ec2.InstanceType.of(_ec2.InstanceClass.BURSTABLE4_GRAVITON, _ec2.InstanceSize.MICRO),
            security_groups=[self.rds_security_group],
        )

        # Lambda Layer
        self.layer = _lambda.LayerVersion(
            self, f"{config.stage}-9c-arena-lambda-layer",
            code=_lambda.AssetCode("layer/"),
            description="Lambda layer for 9c Arena Service",
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_10,
            ],
            removal_policy=RemovalPolicy.DESTROY,
        )
