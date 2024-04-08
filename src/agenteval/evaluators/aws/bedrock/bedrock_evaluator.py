import json

from agenteval.evaluators.aws import AWSEvaluator

_BEDROCK_RUNTIME_BOTO3_NAME = "bedrock-runtime"


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
