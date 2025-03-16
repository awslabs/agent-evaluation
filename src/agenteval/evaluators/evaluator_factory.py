# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel

from agenteval.evaluators import BaseEvaluator
from agenteval.evaluators.canonical.evaluator import CanonicalEvaluator
from agenteval.evaluators.model_config.bedrock_model_config import BedrockModelConfig
from agenteval.evaluators.model_config.preconfigured_model_configs import (
    DEFAULT_CLAUDE_3_5_MODEL_CONFIG,
    DEFAULT_CLAUDE_3_MODEL_CONFIG,
    DEFAULT_CLAUDE_HAIKU_3_5_US_MODEL_CONFIG,
    DEFAULT_CLAUDE_US_3_7_MODEL_CONFIG,
    DEFAULT_LLAMA_3_3_70B_US_MODEL_CONFIG,
)
from agenteval.targets import BaseTarget
from agenteval.test import Test

_EVALUATOR_METHOD_MAP = {
    "canonical": CanonicalEvaluator,
}

_DEFAULT_MODEL_CONFIG_MAP = {
    "claude-3": DEFAULT_CLAUDE_3_MODEL_CONFIG,
    "claude-3_5": DEFAULT_CLAUDE_3_5_MODEL_CONFIG,
    "claude-3_7-us": DEFAULT_CLAUDE_US_3_7_MODEL_CONFIG,
    "claude-haiku-3_5-us": DEFAULT_CLAUDE_HAIKU_3_5_US_MODEL_CONFIG,
    "llama-3_3-us": DEFAULT_LLAMA_3_3_70B_US_MODEL_CONFIG,
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
        reserved_config_keys = {"eval_method", "model", "custom_config"}
        evaluator_cls = self._get_evaluator_class()
        return evaluator_cls(
            test=test,
            target=target,
            work_dir=work_dir,
            model_config=self._get_bedrock_model_config(),
            **{k: v for k, v in self.config.items() if k not in reserved_config_keys},
        )

    def _get_evaluator_class(self) -> type[BaseEvaluator]:
        if "eval_method" in self.config:
            return _EVALUATOR_METHOD_MAP[self.config["eval_method"]]
        else:
            return CanonicalEvaluator

    """
    If the use passes in both an id and a request body, create a custom config instance; otherwise use a default config for the specified model
    """

    def _get_bedrock_model_config(self) -> BedrockModelConfig:
        if "custom_config" in self.config:
            return BedrockModelConfig(
                model_id=self.config["custom_config"]["model_id"],
                request_body=self.config["custom_config"]["request_body"],
            )
        else:
            return _DEFAULT_MODEL_CONFIG_MAP[self.config["model"]]
