from __future__ import annotations

import importlib
import logging
import os
import sys
from typing import Optional, Union

import yaml
from pydantic import BaseModel, model_validator

from agenteval import defaults
from agenteval.evaluators import BaseEvaluator, ClaudeEvaluator
from agenteval.targets import (
    BaseTarget,
    BedrockAgentTarget,
    QBusinessTarget,
    SageMakerEndpointTarget,
)
from agenteval.task import Task

_PLAN_FILE_NAME = "agenteval.yaml"

_INIT_PLAN = {
    "evaluator": {"type": "bedrock-claude", "model": "claude-sonnet"},
    "target": {
        "type": "bedrock-agent",
        "bedrock_agent_id": None,
        "bedrock_agent_alias_id": None,
    },
    "tasks": [
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
    tasks: list[Task]

    @model_validator(mode="after")
    def check_task_names_unique(self) -> Plan:
        unique_names = len(set(task.name for task in self.tasks))

        if unique_names != len(self.tasks):
            raise ValueError("Task names must be unique")

        return self

    @classmethod
    def load(cls, plan_dir: Optional[str]) -> Plan:
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)

        plan = cls._load_yaml(plan_path)
        return cls(
            evaluator_config=EvaluatorConfig(**plan.get("evaluator")),
            target_config=TargetConfig(**plan.get("target")),
            tasks=cls._load_tasks(plan.get("tasks")),
        )

    def create_evaluator(self, task: Task, target: BaseTarget) -> BaseEvaluator:
        if self.evaluator_config.type in _EVALUATOR_MAP:
            evaluator_cls = _EVALUATOR_MAP[self.evaluator_config.type]
        else:
            evaluator_cls = self._get_class(self.evaluator_config)

            if not issubclass(evaluator_cls, BaseEvaluator):
                raise TypeError(f"{evaluator_cls} is not a Evaluator subclass")

        return evaluator_cls(
            task=task,
            target=target,
            **self.evaluator_config.model_dump(exclude="type"),
        )

    def create_target(
        self,
    ) -> BaseTarget:
        if self.target_config.type in _TARGET_MAP:
            target_cls = _TARGET_MAP[self.target_config.type]
        else:
            target_cls = self._get_class(self.target_config)

            if not issubclass(target_cls, BaseTarget):
                raise TypeError(f"{target_cls} is not a Target subclass")

        return target_cls(**self.target_config.model_dump(exclude="type"))

    def _get_class(self, config: Union[EvaluatorConfig, TargetConfig]) -> type:
        module_path, class_name = config.type.rsplit(".", 1)
        return self._import_class(module_path, class_name)

    @staticmethod
    def _import_class(module_path: str, class_name: str) -> type[BaseTarget]:
        module = importlib.import_module(module_path)
        target_cls = getattr(module, class_name)
        return target_cls

    @staticmethod
    def _load_yaml(path: str) -> dict:
        with open(path) as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def _load_tasks(task_config: list[dict]) -> list[Task]:
        tasks = []
        for t in task_config:
            tasks.append(
                Task(
                    name=t.get("name"),
                    steps=t.get("steps"),
                    expected_results=t.get("expected_results"),
                    initial_prompt=t.get("initial_prompt"),
                    max_turns=t.get("max_turns", defaults.MAX_TURNS),
                )
            )
        return tasks

    @staticmethod
    def init_plan(plan_dir: Optional[str]) -> str:
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)

        # check if plan exists
        if os.path.exists(plan_path):
            raise FileExistsError(f"Test plan already exists at {plan_path}")

        with open(plan_path, "w") as stream:
            yaml.safe_dump(_INIT_PLAN, stream, sort_keys=False)

        return plan_path
