import json
from abc import ABC, abstractmethod
from typing import Optional

import boto3
from botocore.client import BaseClient

from agenteval.targets import BaseTarget
from agenteval.task import Task, TaskResult

_USER = "USER"
_AGENT = "AGENT"
_START_TURN_COUNT = 0
_BEDROCK_RUNTIME_BOTO3_NAME = "bedrock-runtime"


class BaseEvaluator(ABC):
    """The `BaseEvaluator` abstract base class defines the common interface for evaluator
    classes.

    Attributes:
        task (Task): The task being evaluated
        target (BaseTarget): The target agent being evaluated
        session (list[tuple]): The session log
        trace (list[str]): The trace log
        turns (int): The number of turns in the session
    """

    def __init__(self, task: Task, target: BaseTarget):
        """Initialize the evaluator instance for a given `Task` and `Target`.

        When initialized, the instance will contain empty `session` and `trace` logs,
        and `turns` will start at `0`.

        - Use `add_turn` to record a turn in the `session` and increment the `turn` counter by `1`.
        - Use `add_to_trace` to add an entry to the `trace`.

        Args:
            task (Task): The task being evaluated
            target (BaseTarget): The target agent being evaluated
        """
        self.task = task
        self.target = target
        self.session: list[tuple] = []
        self.trace: list[str] = []
        self.turns: int = _START_TURN_COUNT

    def add_to_trace(self, entry: str) -> None:
        """Add an entry to the trace log.

        Args:
            entry (str): The string to add to the trace
        """
        self.trace.append(entry)

    def add_turn(self, user_input: str, target_response: str) -> None:
        """Record a turn in the session log.

        Args:
            user_input (str): The user's input
            target_response (str): The target's response

        Increments the `turn` counter by `1`.
        """
        self.session.extend([(_USER, user_input), (_AGENT, target_response)])
        self.turns += 1

    @abstractmethod
    def run(self) -> TaskResult:
        """Run evaluation on a task.

        Returns:
            TaskResult: The result of the evaluation
        """
        pass


class AWSEvaluator(BaseEvaluator):
    """An evaluator that depends on an AWS resource.

    Attributes:
        boto3_client (BaseClient): A `boto3` client.
    """

    def __init__(
        self,
        boto3_service_name: str,
        aws_profile: Optional[str] = None,
        aws_region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize the AWS evaluator.

        Args:
            boto3_service_name (str): The `boto3` service name (e.g `"bedrock-runtime"`)
            aws_profile (str, optional): The AWS profile name
            aws_region (str, optional): The AWS region
            endpoint_url (str, optional): The endpoint URL for the AWS service
            **kwargs : Arguments for the BaseEvaluator initializer
        """
        super().__init__(**kwargs)

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
            boto3_service_name (str): The `boto3` service name (e.g `"bedrock-runtime"`)
            aws_profile (str, optional): The AWS profile name
            aws_region (str, optional): The AWS region
            endpoint_url (str, optional): The endpoint URL for the AWS service

        Returns:
            BaseClient
        """
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        return session.client(boto3_service_name, endpoint_url=endpoint_url)


class BedrockEvaluator(AWSEvaluator):
    """An evaluator that invokes a model on Amazon Bedrock."""

    def __init__(self, model_id: str, **kwargs):
        """
        Initialize the Bedrock evaluator

        Args:
            model_id (str): The ID of the Bedrock model used to run evaluation
            **kwargs: Additional arguments passed to the parent class initializer
        """
        super().__init__(boto3_service_name=_BEDROCK_RUNTIME_BOTO3_NAME, **kwargs)

        self._model_id = model_id

    def invoke_model(self, request_body: dict) -> dict:
        """
        Invoke the Bedrock model using the `boto3_client`. This method will convert
        a request dictionary to a JSON string before passing it to the `InvokeModel` API.

        Refer to the `boto3` documentation for more details.

        Args:
            request_body (dict): The request payload as a dictionary

        Returns:
            dict: The response from the model invocation

        """
        return self.boto3_client.invoke_model(
            modelId=self._model_id, body=json.dumps(request_body)
        )
