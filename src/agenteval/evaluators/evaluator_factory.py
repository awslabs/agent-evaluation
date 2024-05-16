from pydantic import BaseModel

from agenteval.evaluators import BaseEvaluator
from agenteval.evaluators.claude_3 import Claude3Evaluator
from agenteval.targets import BaseTarget
from agenteval.test import Test

_EVALUATOR_MAP = {
    "claude-3": Claude3Evaluator,
}


class EvaluatorFactory(BaseModel):
    config: dict

    def create(self, test: Test, target: BaseTarget, work_dir: str) -> BaseEvaluator:
        evaluator_cls = self._get_evaluator_class()
        return evaluator_cls(
            test=test,
            target=target,
            work_dir=work_dir,
            **{k: v for k, v in self.config.items() if k != "model"}
        )

    def _get_evaluator_class(self) -> type[BaseEvaluator]:
        return _EVALUATOR_MAP[self.config["model"]]
