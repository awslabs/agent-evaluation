from pydantic import BaseModel

from agenteval.targets import BaseTarget
from agenteval.targets.bedrock_agent import BedrockAgentTarget
from agenteval.targets.bedrock_knowledge_base import BedrockKnowledgeBaseTarget
from agenteval.targets.q_business import QBusinessTarget
from agenteval.targets.sagemaker_endpoint import SageMakerEndpointTarget
from agenteval.utils import import_class

_TARGET_MAP = {
    "bedrock-agent": BedrockAgentTarget,
    "q-business": QBusinessTarget,
    "sagemaker-endpoint": SageMakerEndpointTarget,
    "bedrock-knowledgebase": BedrockKnowledgeBaseTarget,
}


class TargetFactory(BaseModel):
    config: dict

    def create(self) -> BaseTarget:
        target_cls = self._get_target_class()

        return target_cls(**{k: v for k, v in self.config.items() if k != "type"})

    def _get_target_class(self) -> type[BaseTarget]:
        if self.config["type"] in _TARGET_MAP:
            target_cls = _TARGET_MAP[self.config["type"]]
        else:
            target_cls = import_class(self.config["type"], parent_class=BaseTarget)

        return target_cls
