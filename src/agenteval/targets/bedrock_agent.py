import uuid

from agenteval.targets.target import AWSTarget

_SERVICE_NAME = "bedrock-agent-runtime"


class BedrockAgentTarget(AWSTarget):
    def __init__(self, bedrock_agent_id: str, bedrock_agent_alias_id: str, **kwargs):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        self._bedrock_agent_id = bedrock_agent_id
        self._bedrock_agent_alias_id = bedrock_agent_alias_id
        self._session_id: str = str(uuid.uuid4())

    def invoke(self, prompt: str) -> str:
        args = {
            "agentId": self._bedrock_agent_id,
            "agentAliasId": self._bedrock_agent_alias_id,
            "sessionId": self._session_id,
            "inputText": prompt,
        }

        response = self.boto3_client.invoke_agent(**args)

        stream = response["completion"]
        completion = ""
        for event in stream:
            chunk = event.get("chunk")
            if chunk:
                completion += chunk.get("bytes").decode()
        return completion
