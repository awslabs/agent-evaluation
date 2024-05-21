import uuid

from agenteval import TargetResponse
from agenteval.targets import Boto3Target

_SERVICE_NAME = "lexv2-runtime"


class LexV2Target(Boto3Target):
    def __init__(self, **kwargs):
        super().__init__(boto3_service_name=_SERVICE_NAME)

    def _get_response(self, request_id: str, **kwargs) -> TargetResponse:
        response = self.client.get_session(botId=self.bot_id, botAliasId=self.bot_alias_id, userId=request_id)
        return TargetResponse(response=response, request_id=request_id)

    def _get_request_id(self) -> str:
        return str(uuid.uuid4())

    def invoke(self, prompt: str) -> TargetResponse:
        pass
