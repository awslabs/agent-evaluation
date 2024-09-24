from agenteval import TargetResponse
from agenteval.targets import Boto3Target

_SERVICE_NAME = "bedrock-agent-runtime"


class BedrockKnowledgeBaseTarget(Boto3Target):
    def __init__(self, knowledge_base_id: str, model_id: str, **kwargs):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        aws_region = self.boto3_client.meta.region_name
        self._knowledge_base_id = knowledge_base_id
        self._model_arn = f"arn:aws:bedrock:{aws_region}::foundation-model/{model_id}"
        self._session_id: str = None

    def invoke(self, prompt: str) -> TargetResponse:
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
