# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from agenteval.targets import Boto3Target, TargetResponse

_SERVICE_NAME = "bedrock-agent-runtime"


class BedrockFlowTarget(Boto3Target):
    """A target encapsulating an Amazon Bedrock Flow."""

    def __init__(self, bedrock_flow_id: str, bedrock_flow_alias_id: str, **kwargs):
        """Initialize the target.

        Args:
            bedrock_flow_id (str): The unique identifier of the Bedrock flow.
            bedrock_flow_alias_id (str): The alias of the Bedrock flow.
        """
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)
        self._bedrock_flow_id = bedrock_flow_id
        self._bedrock_flow_alias_id = bedrock_flow_alias_id

    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt.

        Args:
            prompt (str): The prompt as a string.

        Returns:
            TargetResponse
        """
        args = {
            "enableTrace": True,
            "flowIdentifier": self._bedrock_flow_id,
            "flowAliasIdentifier": self._bedrock_flow_alias_id,
            "inputs": [
                {
                    # Although the API implies otherwise, Flows currently seem to be limited to
                    # follow this single-input node pattern anyway:
                    "content": {"document": prompt},
                    "nodeName": "FlowInputNode",
                    "nodeOutputName": "document",
                }
            ],
        }

        response = self.boto3_client.invoke_flow(**args)

        stream = response["responseStream"]
        completion = ""
        trace_data = []

        for event in stream:
            if "flowTraceEvent" in event:
                trace_data.append(event["flowTraceEvent"].get("trace"))
            if "flowOutputEvent" in event:
                output_event = event["flowOutputEvent"]
                # Testing 2024-12 suggests 'nodeType' actually not always present in API (despite
                # the docs?):
                if (
                    "nodeType" not in output_event
                    or output_event["nodeType"] == "FlowOutputNode"
                ):
                    completion += output_event.get("content", {}).get("document", "")

            errs = {k: v for k, v in event.items() if k.endswith("Exception")}
            if errs:
                raise ValueError(errs)

        return TargetResponse(
            response=completion, data={"bedrock_flow_trace": trace_data}
        )
