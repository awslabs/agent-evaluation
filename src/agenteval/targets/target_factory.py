# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel

from agenteval.targets import BaseTarget
from agenteval.targets.bedrock_agent import BedrockAgentTarget
from agenteval.targets.bedrock_flow import BedrockFlowTarget
from agenteval.targets.bedrock_knowledge_base import BedrockKnowledgeBaseTarget
from agenteval.targets.lexv2 import LexV2Target
from agenteval.targets.q_business import QBusinessTarget
from agenteval.targets.sagemaker_endpoint import SageMakerEndpointTarget
from agenteval.utils import import_class

_TARGET_MAP = {
    "bedrock-agent": BedrockAgentTarget,
    "bedrock-flow": BedrockFlowTarget,
    "q-business": QBusinessTarget,
    "sagemaker-endpoint": SageMakerEndpointTarget,
    "bedrock-knowledge-base": BedrockKnowledgeBaseTarget,
    "lex-v2": LexV2Target,
}


class TargetFactory(BaseModel):
    """A factory for creating instances of `BaseTarget` subclasses.

    Attributes:
        config: A dictionary containing the configuration parameters
            needed to create a `BaseTarget` instance.
    """

    config: dict

    def create(self) -> BaseTarget:
        """Create an instance of the target class specified in the configuration.

        Returns:
            BaseTarget: An instance of the target class, with the configuration
                parameters applied.
        """
        target_cls = self._get_target_class()

        return target_cls(**{k: v for k, v in self.config.items() if k != "type"})

    def _get_target_class(self) -> type[BaseTarget]:
        if self.config["type"] in _TARGET_MAP:
            target_cls = _TARGET_MAP[self.config["type"]]
        else:
            target_cls = import_class(self.config["type"], parent_class=BaseTarget)

        return target_cls
