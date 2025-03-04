# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from agenteval.evaluators.model_config.bedrock_model_config import BedrockModelConfig

""""
# NOTE: Models that are prefixed with `us.` are not supported by Bedrock with on demand inference, so we specify
# the default USA cross region inference profile
# doc: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html
"""

# Claude Models

DEFAULT_CLAUDE_3_MODEL_CONFIG = BedrockModelConfig(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    request_body={
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "system": None,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": None},
                ],
            }
        ],
        "temperature": 0,
        "top_p": 1,
        "top_k": 250,
    },
)

DEFAULT_CLAUDE_3_5_MODEL_CONFIG = BedrockModelConfig(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    request_body={
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "system": None,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": None},
                ],
            }
        ],
        "temperature": 0,
        "top_p": 1,
        "top_k": 250,
    },
)

DEFAULT_CLAUDE_US_3_7_MODEL_CONFIG = BedrockModelConfig(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    request_body={
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "system": None,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": None},
                ],
            }
        ],
        "temperature": 0,
        "top_p": 1,
        "top_k": 250,
    },
)

DEFAULT_CLAUDE_HAIKU_3_5_US_MODEL_CONFIG = BedrockModelConfig(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    request_body={
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "system": None,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": None},
                ],
            }
        ],
        "temperature": 0,
        "top_p": 1,
        "top_k": 250,
    },
)

# LLama Models
DEFAULT_LLAMA_3_3_70B_US_MODEL_CONFIG = BedrockModelConfig(
    model_id="us.meta.llama3-3-70b-instruct-v1:0",
    request_body={
        "prompt": None,
        "max_gen_len": 300,
        "temperature": 0,
        "top_p": 1,
    },
)
