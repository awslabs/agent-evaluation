from typing import Optional

from agenteval.target_response import TargetResponse
from agenteval.targets import Boto3Target

_SERVICE_NAME = "qbusiness"


class QBusinessTarget(Boto3Target):
    def __init__(
        self,
        q_business_application_id: str,
        q_business_user_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)

        self._chat_sync_args = {"applicationId": q_business_application_id}
        if q_business_user_id:
            self._chat_sync_args["userId"] = q_business_user_id

    def invoke(self, prompt: str) -> str:
        self._chat_sync_args["userMessage"] = prompt

        response = self.boto3_client.chat_sync(**self._chat_sync_args)

        if "conversationId" not in self._chat_sync_args:
            self._chat_sync_args["conversationId"] = response["conversationId"]

        self._chat_sync_args["parentMessageId"] = response["systemMessageId"]

        return TargetResponse(response=response["systemMessage"])
