from __future__ import annotations

import logging
import os
import sys
from typing import Optional

import yaml
from pydantic import BaseModel, model_validator

from agenteval import defaults
from agenteval.evaluators import BaseEvaluator
from agenteval.evaluators.aws.bedrock import ClaudeEvaluator
from agenteval.targets import BaseTarget
from agenteval.targets.aws import (
    BedrockAgentTarget,
    QBusinessTarget,
    SageMakerEndpointTarget,
)
from agenteval.test import Test
from agenteval.utils import import_class

_PLAN_FILE_NAME = "agenteval.yml"

_INIT_PLAN = {
    "evaluator": {"type": "bedrock-claude"},
    "target": {
        "type": "bedrock-agent",
        "bedrock_agent_id": None,
        "bedrock_agent_alias_id": None,
    },
    "tests": [
        {
            "name": "RetrieveMissingDocuments",
            "steps": ["Ask agent for a list of missing documents for claim-006"],
            "expected_results": ["The agent returns a list of missing documents."],
        }
    ],
}

_EVALUATOR_MAP = {"bedrock-claude": ClaudeEvaluator}

_TARGET_MAP = {
    "bedrock-agent": BedrockAgentTarget,
    "q-business": QBusinessTarget,
    "sagemaker-endpoint": SageMakerEndpointTarget,
}

sys.path.append(".")
logger = logging.getLogger(__name__)


class EvaluatorConfig(BaseModel, extra="allow"):
    type: str


class TargetConfig(BaseModel, extra="allow"):
    type: str


class Plan(BaseModel, validate_assignment=True, arbitrary_types_allowed=True):
    evaluator_config: EvaluatorConfig
    target_config: TargetConfig
    tests: list[Test]

    @model_validator(mode="after")
    def check_test_names_unique(self) -> Plan:
        unique_names = len(set(test.name for test in self.tests))

        if unique_names != len(self.tests):
            raise ValueError("Test names must be unique")

        return self

    @classmethod
    def load(cls, plan_dir: Optional[str]) -> Plan:
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)

        plan = cls._load_yaml(plan_path)
        return cls(
            evaluator_config=EvaluatorConfig(**plan.get("evaluator")),
            target_config=TargetConfig(**plan.get("target")),
            tests=cls._load_tests(plan.get("tests")),
        )

    def create_evaluator(
        self, test: Test, target: BaseTarget, work_dir: str
    ) -> BaseEvaluator:
        if self.evaluator_config.type in _EVALUATOR_MAP:
            evaluator_cls = _EVALUATOR_MAP[self.evaluator_config.type]
        else:
            evaluator_cls = import_class(
                self.evaluator_config.type, parent_class=BaseEvaluator
            )

        return evaluator_cls(
            test=test,
            target=target,
            work_dir=work_dir,
            **self.evaluator_config.model_dump(exclude="type"),
        )

    def create_target(
        self,
    ) -> BaseTarget:
        if self.target_config.type in _TARGET_MAP:
            target_cls = _TARGET_MAP[self.target_config.type]
        else:
            target_cls = import_class(self.target_config.type, parent_class=BaseTarget)

        return target_cls(**self.target_config.model_dump(exclude="type"))

    @staticmethod
    def _load_yaml(path: str) -> dict:
        with open(path) as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def _load_tests(test_config: list[dict]) -> list[Test]:
        tests = []
        for t in test_config:
            tests.append(
                Test(
                    name=t.get("name"),
                    steps=t.get("steps"),
                    expected_results=t.get("expected_results"),
                    initial_prompt=t.get("initial_prompt"),
                    max_turns=t.get("max_turns", defaults.MAX_TURNS),
                    hook=t.get("hook"),
                )
            )
        return tests

    @staticmethod
    def init_plan(plan_dir: Optional[str]) -> str:
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)

        # check if plan exists
        if os.path.exists(plan_path):
            raise FileExistsError(f"Test plan already exists at {plan_path}")

        with open(plan_path, "w") as stream:
            yaml.safe_dump(_INIT_PLAN, stream, sort_keys=False)

        return plan_path
