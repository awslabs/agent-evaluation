# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid

from agenteval import TargetResponse
from agenteval.targets import Boto3Target

_SERVICE_NAME = "bedrock-agent-runtime"


class BedrockAgentTarget(Boto3Target):
    """A target encapsulating an Amazon Bedrock agent."""

    def __init__(self, bedrock_agent_id: str, bedrock_agent_alias_id: str, **kwargs):
        """Initialize the target.

        Args:
            bedrock_agent_id (str): The unique identifier of the Bedrock agent.
            bedrock_agent_alias_id (str): The alias of the Bedrock agent.

        """
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        self._bedrock_agent_id = bedrock_agent_id
        self._bedrock_agent_alias_id = bedrock_agent_alias_id
        self._session_id: str = str(uuid.uuid4())

    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt.

        Args:
            prompt (str): The prompt as a string.

        Returns:
            TargetResponse
        """
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
