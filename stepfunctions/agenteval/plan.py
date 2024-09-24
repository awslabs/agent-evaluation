# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging
import os
import sys
from typing import Optional

import yaml
from pydantic import BaseModel, model_validator

from agenteval import defaults
from agenteval.evaluators import EvaluatorFactory
from agenteval.targets import TargetFactory
from agenteval.test import Test

_PLAN_FILE_NAME = "agenteval.yml"

_INIT_PLAN = {
    "evaluator": {"model": "claude-3"},
    "target": {
        "type": "bedrock-agent",
        "bedrock_agent_id": None,
        "bedrock_agent_alias_id": None,
    },
    "tests": {
        "retrieve_missing_documents": {
            "steps": ["Ask agent for a list of missing documents for claim-006."],
            "expected_results": ["The agent returns a list of missing documents."],
        }
    },
}


sys.path.append(".")
logger = logging.getLogger(__name__)


class Plan(BaseModel, validate_assignment=True, arbitrary_types_allowed=True):
    evaluator_factory: EvaluatorFactory
    target_factory: TargetFactory
    tests: list[Test]

    @model_validator(mode="after")
    def check_test_names_unique(self) -> Plan:
        unique_names = len(set(test.name for test in self.tests))

        if unique_names != len(self.tests):
            raise ValueError("Test names must be unique")

        return self

    @classmethod
    def load(cls, plan_dir: Optional[str], filter: str) -> Plan:
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)
        plan = cls._load_yaml(plan_path)

        return cls(
            evaluator_factory=EvaluatorFactory(config=plan["evaluator"]),
            target_factory=TargetFactory(config=plan["target"]),
            tests=cls._load_tests(plan["tests"], filter),
        )

    @staticmethod
    def _load_yaml(path: str) -> dict:
        with open(path) as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def _load_tests(test_config: list[dict], filter: str) -> list[Test]:
        tests = []

        if filter:
            names = Plan._parse_filter(filter)
        else:
            names = test_config.keys()

        for name in names:
            config = test_config[name]
            tests.append(
                Test(
                    name=name,
                    steps=config["steps"],
                    expected_results=config["expected_results"],
                    initial_prompt=config.get("initial_prompt"),
                    max_turns=config.get("max_turns", defaults.MAX_TURNS),
                    hook=config.get("hook"),
                )
            )

        return tests

    @staticmethod
    def _parse_filter(filter: str) -> list[str]:
        return [n.strip() for n in filter.split(",")]

    @staticmethod
    def init_plan(plan_dir: Optional[str]) -> str:
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)

        # check if plan exists
        if os.path.exists(plan_path):
            raise FileExistsError(f"Test plan already exists at {plan_path}")

        with open(plan_path, "w") as stream:
            yaml.safe_dump(_INIT_PLAN, stream, sort_keys=False)

        return plan_path
