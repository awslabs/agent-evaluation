# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid
import time
import random
from botocore.exceptions import ClientError

from agenteval.targets import Boto3Target, TargetResponse

import logging

logger = logging.getLogger(__name__)

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
        completion = ""
        trace_data = []

        back_off = 0.01  # In seconds.
        done = False
        while not done:
            try:
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

                if back_off > 0.01:
                    logger.debug(
                        f"BedrockAgentTarget.invoke, success after backoff. back_off={back_off}"
                    )
                done = True

            except ClientError as exception_obj:
                error_code = exception_obj.response["Error"]["Code"]
                if error_code == "throttlingException":
                    logger.debug(
                        f"BedrockAgentTarget.invoke, throttle. error_code={error_code}, back_off={back_off}"
                    )
                    time.sleep(
                        back_off
                        * random.uniform(
                            1, 2
                        )  # Random backoff between back_off and 2x back_off seconds.
                    )
                    back_off *= 2  # Exponential backoff.

                else:
                    logger.warning(
                        f"BedrockAgentTarget.invoke, unexpected error. error_code={error_code}"
                    )
                    return TargetResponse(
                        response=completion, data={"bedrock_agent_trace": trace_data}
                    )

        return TargetResponse(
            response=completion, data={"bedrock_agent_trace": trace_data}
        )
