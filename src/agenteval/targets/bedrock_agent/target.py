import uuid

from agenteval.targets import Boto3Target, TargetResponse

_SERVICE_NAME = "bedrock-agent-runtime"


class BedrockAgentTarget(Boto3Target):
    def __init__(self, bedrock_agent_id: str, bedrock_agent_alias_id: str, **kwargs):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        self._bedrock_agent_id = bedrock_agent_id
        self._bedrock_agent_alias_id = bedrock_agent_alias_id
        self._session_id: str = str(uuid.uuid4())

    def invoke(self, prompt: str) -> TargetResponse:
        args = {
            "agentId": self._bedrock_agent_id,
            "agentAliasId": self._bedrock_agent_alias_id,
            "sessionId": self._session_id,
            "inputText": prompt,
            "enableTrace": True,
        }

        response = self.boto3_client.invoke_agent(**args)

        stream = response["completion"]
        completion = ""
        trace_data = []

        for event in stream:
            chunk = event.get("chunk")
            event_trace = event.get("trace")
            if chunk:
                completion += chunk.get("bytes").decode()
            if event_trace:
                trace_data.append(event_trace.get("trace"))

        return TargetResponse(
            response=completion, data={"bedrock_agent_trace": trace_data}
        )
