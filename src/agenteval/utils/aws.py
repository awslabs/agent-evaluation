# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config

_RETRY_MODE = "adaptive"


def create_boto3_client(
    boto3_service_name: str,
    aws_profile: Optional[str],
    aws_region: Optional[str],
    endpoint_url: Optional[str],
    max_retry: int,
) -> BaseClient:
    """Create a `boto3` client.

    Args:
        boto3_service_name (str): The `boto3` service name (e.g `"bedrock-runtime"`).
        aws_profile (Optional[str]): The AWS profile name.
        aws_region (Optional[str]): The AWS region.
        endpoint_url (Optional[str]): The endpoint URL for the AWS service.
        max_retry (int): The maximum number of retry attempts.

    Returns:
        BaseClient
    """

    config = Config(retries={"max_attempts": max_retry, "mode": _RETRY_MODE})

    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
    return session.client(boto3_service_name, endpoint_url=endpoint_url, config=config)
