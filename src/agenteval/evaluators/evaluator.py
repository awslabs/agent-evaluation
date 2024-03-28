import json
from abc import ABC, abstractmethod
from typing import Optional

import boto3
from botocore.client import BaseClient

from agenteval.conversation_handler import ConversationHandler
from agenteval.hook import Hook
from agenteval.targets import BaseTarget
from agenteval.test import Test
from agenteval.test_result import TestResult
from agenteval.trace_handler import TraceHandler
from agenteval.utils import import_class, validate_subclass

_BEDROCK_RUNTIME_BOTO3_NAME = "bedrock-runtime"


class BaseEvaluator(ABC):
    """The `BaseEvaluator` abstract base class defines the common interface for evaluator
    classes.

    Attributes:
        test (Test): The test case.
        target (BaseTarget): The target agent being evaluated.
        conversation (ConversationHandler): Conversation handler for capturing the interaction
            between the evaluator (user) and target (agent).
        trace (TraceHandler): Trace handler for capturing steps during evaluation.
        test_result (TestResult): The result of the test which is set in `BaseEvaluator.run`.
    """

    def __init__(self, test: Test, target: BaseTarget):
        """Initialize the evaluator instance for a given `Test` and `Target`.

        Args:
            test (Test): The test case.
            target (BaseTarget): The target agent being evaluated.
        """
        self.test = test
        self.target = target
        self.conversation = ConversationHandler()
        self.trace = TraceHandler(test_name=test.name)
        self.test_result = None

    @abstractmethod
    def evaluate(self) -> TestResult:
        """Conduct a test.

        Returns:
            TestResult: The result of the test.
        """
        pass

    def _get_hook_cls(self, hook: Optional[str]) -> Optional[type[Hook]]:
        if hook:
            hook_cls = import_class(hook)
            validate_subclass(hook_cls, Hook)
            return hook_cls

    def run(self) -> TestResult:
        """
        Run the evaluator within a trace context manager and run hooks
        if provided.
        """

        hook_cls = self._get_hook_cls(self.test.hook)

        with self.trace:
            if hook_cls:
                hook_cls.pre_evaluate(self.test, self.trace)
            self.test_result = self.evaluate()
            if hook_cls:
                hook_cls.post_evaluate(self.test, self.test_result, self.trace)

        return self.test_result


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
            boto3_service_name (str): The `boto3` service name (e.g `"bedrock-runtime"`).
            aws_profile (str, optional): The AWS profile name.
            aws_region (str, optional): The AWS region.
            endpoint_url (str, optional): The endpoint URL for the AWS service.
            **kwargs : Arguments for the BaseEvaluator initializer.
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
            boto3_service_name (str): The `boto3` service name (e.g `"bedrock-runtime"`).
            aws_profile (str, optional): The AWS profile name.
            aws_region (str, optional): The AWS region.
            endpoint_url (str, optional): The endpoint URL for the AWS service.

        Returns:
            BaseClient
        """
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        return session.client(boto3_service_name, endpoint_url=endpoint_url)


class BedrockEvaluator(AWSEvaluator):
    """An evaluator that invokes a model on Amazon Bedrock."""

    def __init__(self, model_id: str, **kwargs):
        """
        Initialize the Bedrock evaluator.

        Args:
            model_id (str): The ID of the Bedrock model used to run evaluation.
            **kwargs: Additional arguments passed to the parent class initializer.
        """
        super().__init__(boto3_service_name=_BEDROCK_RUNTIME_BOTO3_NAME, **kwargs)

        self._model_id = model_id

    def invoke_model(self, request_body: dict) -> dict:
        """
        Invoke the Bedrock model using the `boto3_client`. This method will convert
        a request dictionary to a JSON string before passing it to the `InvokeModel` API.

        Refer to the `boto3` documentation for more details.

        Args:
            request_body (dict): The request payload as a dictionary.

        Returns:
            dict: The response from the model invocation.

        """
        return self.boto3_client.invoke_model(
            modelId=self._model_id, body=json.dumps(request_body)
        )
