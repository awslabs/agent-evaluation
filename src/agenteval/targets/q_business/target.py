# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Optional

from agenteval.targets import Boto3Target, TargetResponse

_SERVICE_NAME = "qbusiness"


class QBusinessTarget(Boto3Target):
    """A target encapsulating an Amazon Q Business application."""

    def __init__(
        self,
        q_business_application_id: str,
        q_business_user_id: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the target.

        Args:
            q_business_application_id (str): The unique identifier of the Amazon Q application.
            q_business_user_id (Optional[str]): The identifier of the Amazon Q user.

        """
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)

        self._chat_sync_args = {"applicationId": q_business_application_id}
        if q_business_user_id:
            self._chat_sync_args["userId"] = q_business_user_id

    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt.

        Args:
            prompt (str): The prompt as a string.

        Returns:
            TargetResponse
        """
        self._chat_sync_args["userMessage"] = prompt

        response = self.boto3_client.chat_sync(**self._chat_sync_args)

        if "conversationId" not in self._chat_sync_args:
            self._chat_sync_args["conversationId"] = response["conversationId"]

        self._chat_sync_args["parentMessageId"] = response["systemMessageId"]

        return TargetResponse(response=response["systemMessage"])
