# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid

from agenteval.targets import Boto3Target, TargetResponse

_SERVICE_NAME = "lexv2-runtime"


class LexV2Target(Boto3Target):
    def __init__(self, bot_id: str, bot_alias_id: str, locale_id: str, **kwargs):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        self._bot_id = bot_id
        self._bot_alias_id = bot_alias_id
        self._locale_id = locale_id
        self._session_id = str(uuid.uuid4())

    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt.

        Args:
            prompt(str): The prompt to send to the target.

        Returns:
            TargetResponse: The response from the target.
        """
        args = {
            "botId": self._bot_id,
            "botAliasId": self._bot_alias_id,
            "localeId": self._locale_id,
            "sessionId": self._session_id,
            "text": prompt,
        }

        response = self.boto3_client.recognize_text(**args)
        if response["sessionState"]["dialogAction"]["type"] == "Close":
            completion = "Completed"
        else:
            completion = response["messages"][0]["content"]
        interpretation_data = [response]

        return TargetResponse(
            response=completion, data={"lexv2_interpretation_data": interpretation_data}
        )
