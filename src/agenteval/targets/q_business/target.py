from agenteval.target_response import TargetResponse
from agenteval.targets import Boto3Target

_SERVICE_NAME = "qbusiness"


class QBusinessTarget(Boto3Target):
    def __init__(
        self, q_business_application_id: str, q_business_user_id: str, **kwargs
    ):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)

        self._q_business_application_id = q_business_application_id
        self._q_business_user_id = q_business_user_id
        self._parent_message_id: str = ""
        self._conversation_id: str = ""

    def invoke(self, prompt: str) -> str:
        args = {
            "applicationId": self._q_business_application_id,
            "userId": self._q_business_user_id,
            "userMessage": prompt,
        }

        if self._conversation_id and self._parent_message_id:
            args["conversationId"] = self._conversation_id
            args["parentMessageId"] = self._parent_message_id

        response = self.boto3_client.chat_sync(**args)

        self._parent_message_id = response["systemMessageId"]

        if not self._conversation_id:
            self._conversation_id = response["conversationId"]

        return TargetResponse(response=response["systemMessage"])
