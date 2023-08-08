import os

import aws_cdk as cdk_core
import boto3
from aws_cdk import (
    RemovalPolicy, Stack,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_lambda_event_sources as _evt_src,
    aws_events as _events,
    aws_events_targets as _event_targets,
)
from constructs import Construct

from common import COMMON_LAMBDA_EXCLUDE, Config
from worker import WORKER_LAMBDA_EXCLUDE

class WorkerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        config: Config = kwargs.pop("config")
        shared_stack = kwargs.pop("shared_stack", None)
        if shared_stack is None:
            raise ValueError("Shared stack not found. Please provide shared stack.")
        super().__init__(scope, construct_id, **kwargs)

        # # Lambda layer
        # layer = _lambda.LayerVersion(
        #     self, f"{config.stage}-9c-arena-worker-lambda-layer",
        #     code=_lambda.AssetCode("worker/layer/"),
        #     description="Lambda layer for 9c arena service worker",
        #     compatible_runtimes=[
        #         _lambda.Runtime.PYTHON_3_10,
        #     ],
        #     removal_policy=RemovalPolicy.DESTROY,
        # )

        # Lambda Role
        role = _iam.Role(
            self, f"{config.stage}-9c-iap-worker-role",
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
            ]
        )
        # DB Password
        role.add_to_policy(
            _iam.PolicyStatement(
                actions=["secretsmanager:GetSecretValue"],
                resources=[shared_stack.rds.secret.secret_arn],
            )
        )

        # Environment Variables
        env = {
            "REGION_NAME": config.region_name,
            "STAGE": config.stage,
            "SECRET_ARN": shared_stack.rds.secret.secret_arn,
            "DB_URI": f"postgresql://"
                      f"{shared_stack.credentials.username}:[DB_PASSWORD]"
                      f"@{shared_stack.rds.db_instance_endpoint_address}"
                      f"/arena",
            "HEADLESS": config.headless,
        }

        # Block track + arena info updater Lambda function
        exclude_list = [".idea", ".gitignore", ]
        exclude_list.extend(COMMON_LAMBDA_EXCLUDE)
        exclude_list.extend(WORKER_LAMBDA_EXCLUDE)

        tracker = _lambda.Function(
            self, f"{config.stage}-9c-arena-block-tracker-function",
            function_name=f"{config.stage}-9c-arena-block-tracker",
            runtime=_lambda.Runtime.PYTHON_3_10,
            description="Worker to track 9c blocks and update arena actions",
            code=_lambda.AssetCode("worker/worker/", exclude=exclude_list),
            handler="block_tracker.handle",
            layers=[shared_stack.layer],
            role=role,
            vpc=shared_stack.vpc,
            timeout=cdk_core.Duration.seconds(50),
            environment=env,
            memory_size=256,
        )

        # Every minute
        minute_event_rule = _events.Rule(
            self, f"{config.stage}-9c-arena-tracker-event",
            schedule=_events.Schedule.cron(minute="*")  # Every minute
        )
        minute_event_rule.add_target(_event_targets.LambdaFunction(tracker))
