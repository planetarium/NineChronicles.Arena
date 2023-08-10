import json
from typing import Dict

import boto3


def fetch_secrets(region: str, secret_arn: str) -> Dict:
    sm = boto3.client("secretsmanager", region_name=region)
    resp = sm.get_secret_value(SecretId=secret_arn)
    return json.loads(resp["SecretString"])
