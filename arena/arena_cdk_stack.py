import aws_cdk as cdk_core
from aws_cdk import (
    RemovalPolicy, Stack,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_certificatemanager as _acm,
    aws_apigateway as _apig,
)
from constructs import Construct

from arena import ARENA_LAMBDA_EXCLUDE
from common import Config, COMMON_LAMBDA_EXCLUDE


class ArenaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        config: Config = kwargs.pop("config")
        shared_stack = kwargs.pop("shared_stack", None)
        if shared_stack is None:
            raise ValueError("Shared stack not found. Please provide shared stack.")
        super().__init__(scope, construct_id, **kwargs)

        # Lambda Layer
        layer = _lambda.LayerVersion(
            self, f"{config.stage}-9c-arena-api-lambda-layer",
            code=_lambda.AssetCode("arena/layer/"),
            description="Lambda layer for 9c Arena API Service",
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_10,
            ],
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Lambda Role
        role = _iam.Role(
            self, f"{config.stage}-9c-arena-api-role",
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
            ],
        )
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
            "LOGGING_LEVEL": "INFO",
            "DB_ECHO": "False",
            "HEADLESS": config.headless,
        }

        # Lambda Function
        exclude_list = [".", "*", ".idea", ".gitignore", ".github", ]
        exclude_list.extend(COMMON_LAMBDA_EXCLUDE)
        exclude_list.extend(ARENA_LAMBDA_EXCLUDE)

        function = _lambda.Function(
            self, f"{config.stage}-9c-arena-api-function",
            runtime=_lambda.Runtime.PYTHON_3_10,
            function_name=f"{config.stage}-9c-arena-api",
            description="HTTP API/Backoffice service of NineChronicles.Arena",
            code=_lambda.AssetCode(".", exclude=exclude_list),
            handler="arena.main.handler",
            layers=[layer],
            role=role,
            vpc=shared_stack.vpc,
            timeout=cdk_core.Duration.seconds(15),
            environment=env,
            memory_size=256,
        )

        # ACM & Custom Domain
        if config.stage != "development":
            certificate = _acm.Certificate.from_certificate_arn(
                self, "9c-acm",
                certificate_arn="arn:aws:acm:us-east-1:319679068466:certificate/774ba332-0886-481b-b823-d0c4ab160d37"
            )
            custom_domain = _apig.DomainNameOptions(
                domain_name=f"{'internal-' if config.stage == 'internal' else ''}arena.nine-chronicles.com",
                certificate=certificate,
                security_policy=_apig.SecurityPolicy.TLS_1_2,
                endpoint_type=_apig.EndpointType.EDGE,
            )

        else:
            custom_domain = None

        # API Gateway
        apig = _apig.LambdaRestApi(
            self, f"{config.stage}-9c-arena-arena-apig",
            handler=function,
            deploy_options=_apig.StageOptions(stage_name=config.stage),
            domain_name=custom_domain,
        )
