# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from agenteval.targets import Boto3Target, TargetResponse

_SERVICE_NAME = "bedrock-agent-runtime"


class BedrockKnowledgeBaseTarget(Boto3Target):
    """A target encapsulating an Amazon Bedrock knowledge base."""

    def __init__(self, knowledge_base_id: str, model_id: str, **kwargs):
        """Initialize the target.

        Args:
            knowledge_base_id (str): The unique identifier of the knowledge base that
                is queried and the foundation model used for generation.
            model_id (str): The unique identifier of the foundation model used to
                generate a response.
        """
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        aws_region = self.boto3_client.meta.region_name
        self._knowledge_base_id = knowledge_base_id
        self._model_arn = f"arn:aws:bedrock:{aws_region}::foundation-model/{model_id}"
        self._session_id: str = None

    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt.

        Args:
            prompt (str): The prompt as a string.

        Returns:
            TargetResponse
        """
        args = {
            "input": {
                "text": prompt,
            },
            "retrieveAndGenerateConfiguration": {
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": self._knowledge_base_id,
                    "modelArn": self._model_arn,
                },
            },
        }
        if self._session_id:
            args["sessionId"] = self._session_id

        response = self.boto3_client.retrieve_and_generate(**args)
        generated_text = response["output"]["text"]
        citations = response["citations"]
        self._session_id = response["sessionId"]

        return TargetResponse(
            response=generated_text, data={"bedrock_knowledgebase_citations": citations}
        )
