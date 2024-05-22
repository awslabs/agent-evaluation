# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel

from agenteval.evaluators import BaseEvaluator
from agenteval.evaluators.claude_3 import Claude3Evaluator
from agenteval.targets import BaseTarget
from agenteval.test import Test

_EVALUATOR_MAP = {
    "claude-3": Claude3Evaluator,
}


class EvaluatorFactory(BaseModel):
    """A factory for creating instances of `BaseEvaluator` subclasses.

    Attributes:
        config: A dictionary containing the configuration parameters
            needed to create a `BaseEvaluator` instance.
    """

    config: dict

    def create(self, test: Test, target: BaseTarget, work_dir: str) -> BaseEvaluator:
        """Create an instance of the evaluator class specified in the configuration.

        Args:
            test (Test): The test case.
            target (BaseTarget): The target agent being evaluated.
            work_dir (str): The directory where the test result and trace will be
                generated.

        Returns:
            BaseEvaluator: An instance of the evaluator class, with the configuration
                parameters applied.
        """
        evaluator_cls = self._get_evaluator_class()
        return evaluator_cls(
            test=test,
            target=target,
            work_dir=work_dir,
            **{k: v for k, v in self.config.items() if k != "model"}
        )

    def _get_evaluator_class(self) -> type[BaseEvaluator]:
        return _EVALUATOR_MAP[self.config["model"]]
