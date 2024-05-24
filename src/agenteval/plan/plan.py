# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import concurrent.futures
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Optional

import yaml
from pydantic import BaseModel
from rich.progress import Progress

from agenteval import defaults
from agenteval.evaluators import EvaluatorFactory
from agenteval.plan.exceptions import TestFailureError
from agenteval.plan.logging import log_run_end, log_run_start
from agenteval.run import Run
from agenteval.store import Store
from agenteval.summary import create_markdown_summary
from agenteval.targets import TargetFactory
from agenteval.test import TestSuite
from agenteval.utils import calculate_pass_rate

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
            "expected": {
                "conversation": ["The agent returns a list of missing documents."]
            },
        }
    },
}


sys.path.append(".")
logger = logging.getLogger(__name__)


class Plan(BaseModel):
    """Encapsulates the configurations for a test plan, which includes information
    about the evaluator, the target, the tests to be executed, and various settings
    for running the tests.

    Attributes:
        config: A dictionary containing the test plan configurations.
    """

    config: dict

    @classmethod
    def load(cls, plan_dir: Optional[str] = None) -> Plan:
        """Loads the test plan configurations from YAML.

        Args:
            plan_dir (Optional[str]): The directory containing the test plan.
                If `None`, the current working directory will be used.

        Returns:
            Plan: A `Plan` instance containing the loaded test plan configurations.
        """
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)
        plan = cls._load_yaml(plan_path)
        return cls(config=plan)

    @staticmethod
    def _load_yaml(path: str) -> dict:
        with open(path) as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def init_plan(plan_dir: Optional[str] = None) -> str:
        """Initializes a new test plan configuration YAML file.

        Args:
            plan_dir (Optional[str]): The directory where the YAML file will be stored.
                If `None`, the current working directory will be used.

        Returns:
            str: The path to the YAML file.
        """
        plan_path = os.path.join(plan_dir or os.getcwd(), _PLAN_FILE_NAME)

        # check if plan exists
        if os.path.exists(plan_path):
            logger.error(f"[red]Test plan already exists at {plan_path}")

            raise FileExistsError

        with open(plan_path, "w") as stream:
            yaml.safe_dump(_INIT_PLAN, stream, sort_keys=False)

        logger.info(f"[green]Test plan created at {plan_path}")

        return plan_path

    @staticmethod
    def _resolve_num_threads(num_tests: int, num_threads: Optional[int]) -> int:
        return (
            min(num_tests, defaults.MAX_NUM_THREADS)
            if num_threads is None
            else num_threads
        )

    def run(
        self,
        verbose: bool = False,
        num_threads: Optional[int] = None,
        filter: Optional[str] = None,
        summary_dir: Optional[str] = None,
        backend_store_url: Optional[str] = None,
    ):
        """Run the test plan.

        Args:
            verbose (bool): Whether to enable verbose logging.
            num_threads (Optional[int]): Number of threads used to run tests concurrently.
            filter (Optional[str]): Specifies the test(s) to run, where multiple tests should be seperated using a comma.
            summary_dir (Optional[str]): The directory to save the test summary to.
            backend_store_url (Optional[str]): The database URL of the backend store.
        """
        self._setup_run(filter, num_threads, summary_dir, backend_store_url)

        log_run_start(verbose, self._num_tests, self._num_threads)

        self._run_start_time = datetime.now(timezone.utc)

        with Progress(transient=True) as self._progress:
            self._tracker = self._progress.add_task("running...", total=self._num_tests)
            self._run_concurrent()

        self._run_end_time = datetime.now(timezone.utc)

        self._pass_rate = calculate_pass_rate(self._pass_count, self._num_tests)

        run_id = self._save_run()

        log_run_end(
            verbose,
            self._test_suite.tests,
            self._num_tests,
            self._pass_count,
            self._run_start_time,
            self._run_end_time,
            self._evaluator_input_token_count,
            self._evaluator_output_token_count,
        )

        create_markdown_summary(
            self._summary_dir,
            run_id,
            self._pass_rate,
            self._num_tests,
            self._run_start_time,
            self._run_end_time,
            self._evaluator_input_token_count,
            self._evaluator_output_token_count,
            self._test_suite.tests,
        )

        if self._num_tests != self._pass_count:
            raise TestFailureError

    def _setup_run(
        self,
        filter: Optional[str],
        num_threads: Optional[int],
        summary_dir: Optional[str],
        backend_store_url: Optional[str],
    ):
        self._evaluator_factory = EvaluatorFactory(config=self.config["evaluator"])
        self._target_factory = TargetFactory(config=self.config["target"])
        self._test_suite = TestSuite.load(self.config["tests"], filter)
        self._lock = threading.Lock()
        self._num_tests = self._test_suite.num_tests
        self._num_threads = self._resolve_num_threads(self._num_tests, num_threads)
        self._summary_dir = summary_dir or os.getcwd()
        self._store = Store(backend_store_url)

        self._evaluator_input_token_count = 0
        self._evaluator_output_token_count = 0
        self._pass_count = 0

    def _run_concurrent(self):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self._num_threads
        ) as executor:
            futures = [
                executor.submit(self._run_test, test) for test in self._test_suite
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    raise e

    def _run_test(self, test):
        target = self._target_factory.create()
        evaluator = self._evaluator_factory.create(
            test=test,
            target=target,
        )

        evaluator.run()

        with self._lock:
            if test.test_result.passed is True:
                self._pass_count += 1
            self._evaluator_input_token_count += (
                test.test_result.evaluator_input_token_count
            )
            self._evaluator_output_token_count += (
                test.test_result.evaluator_output_token_count
            )
            self._progress.update(self._tracker, advance=1)

    def _save_run(self) -> int:
        logger.info("Saving run...")
        run_id = self._store.save_run(
            Run(
                start_time=self._run_start_time,
                end_time=self._run_end_time,
                tests=self._test_suite.tests,
            )
        )
        return run_id
