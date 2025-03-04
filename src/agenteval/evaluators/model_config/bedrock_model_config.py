# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from enum import Enum
from typing import Dict


class ModelProvider(Enum):
    META = "meta"
    ANTHROPIC = "anthropic"


@dataclass
class BedrockModelConfig:
    model_id: str
    request_body: Dict

    """
    Match the provider by looking for the provider name in the model_id.
    This should be a robust approach, but if name conflicts are found in the future,
    constructors can explicitly provide the ModelProvider directly.
    Even for provisioned throughput ARN, the modelID will adhere to the matching defined here.
    """

    @property
    def provider(self) -> ModelProvider:
        if "meta" in self.model_id:
            return ModelProvider.META
        elif "anthropic" in self.model_id:
            return ModelProvider.ANTHROPIC
        else:
            raise ValueError(f"Unsupported model ID: {self.model_id}")
