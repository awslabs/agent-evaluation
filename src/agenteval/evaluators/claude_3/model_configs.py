# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
ANTHROPIC_VERSION = "bedrock-2023-05-31"
ROLE = "user"
MAX_TOKENS_TO_SAMPLE = 300
TEMPERATURE = 0
TOP_K = 250
TOP_P = 1
REQUEST_BODY = {
    "anthropic_version": ANTHROPIC_VERSION,
    "max_tokens": MAX_TOKENS_TO_SAMPLE,
    "system": None,
    "messages": [
        {
            "role": ROLE,
            "content": [
                {"type": "text", "text": None},
            ],
        }
    ],
    "temperature": TEMPERATURE,
    "top_p": TOP_P,
    "top_k": TOP_K,
}
