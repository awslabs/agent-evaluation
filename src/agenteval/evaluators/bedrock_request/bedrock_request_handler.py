# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
from typing import Dict

from agenteval.evaluators.model_config.bedrock_model_config import (
    BedrockModelConfig,
    ModelProvider,
)


class BedrockRequestHandler:
    """
    Static class for building requests to and receiving requests from Bedrock depending on the model
    The BedrockModelConfig constructor throws if it doesn't produce a valid ModelProvider, so don't need to handle else cases
    """

    @staticmethod
    def build_request_body(
        request_body: Dict,
        model_config: BedrockModelConfig,
        system_prompt: str,
        prompt: str,
    ) -> Dict:
        if model_config.provider == ModelProvider.META:
            # Source for approach: https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_3/
            request_body["prompt"] = (
                f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}"
                f"<|eot_id|><|start_header_id|>user<|end_header_id|>{prompt}"
                "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
            )
        elif model_config.provider == ModelProvider.ANTHROPIC:
            request_body["system"] = system_prompt
            if "messages" in request_body:
                request_body["messages"][0]["content"][0]["text"] = prompt
        return request_body

    @staticmethod
    def parse_completion_from_response(
        response: Dict, model_config: BedrockModelConfig
    ) -> str:
        response_body = response.get("body").read()
        if model_config.provider == ModelProvider.META:
            completion = json.loads(response_body)["generation"]
        elif model_config.provider == ModelProvider.ANTHROPIC:
            completion = json.loads(response_body)["content"][0]["text"]
        return completion
