from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import boto3
from botocore.client import BaseClient


class BaseTarget(ABC):
    """The `BaseTarget` abstract base class defines the common interface for target
    classes.
    """

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Invoke the target with a prompt and return a response as a string.

        Args:
            prompt: The prompt string to pass to the target

        Returns:
            The target's response as a string
        """
        pass


class AWSTarget(BaseTarget):
    """A target that depends on an AWS resource.

    Attributes:
        boto3_client (BaseClient): A `boto3` client.
    """

    def __init__(
        self,
        boto3_service_name: str,
        aws_profile: Optional[str] = None,
        aws_region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
    ):
        """
        Initialize the AWS target.

        Args:
            boto3_service_name (str): The `boto3` service name (e.g `"bedrock-agent-runtime"`)
            aws_profile (str, optional): The AWS profile name
            aws_region (str, optional): The AWS region
            endpoint_url (str, optional): The endpoint URL for the AWS service
        """
        self.boto3_client = self._create_boto3_client(
            boto3_service_name=boto3_service_name,
            aws_profile=aws_profile,
            aws_region=aws_region,
            endpoint_url=endpoint_url,
        )

    @staticmethod
    def _create_boto3_client(
        boto3_service_name: str,
        aws_profile: Optional[str],
        aws_region: Optional[str],
        endpoint_url: Optional[str],
    ) -> BaseClient:
        """Create a `boto3` client.

        Args:
            boto3_service_name (str): The `boto3` service name (e.g `"bedrock-agent-runtime"`)
            aws_profile (str, optional): The AWS profile name
            aws_region (str, optional): The AWS region
            endpoint_url (str, optional): The endpoint URL for the AWS service

        Returns:
            BaseClient
        """
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        return session.client(boto3_service_name, endpoint_url=endpoint_url)
