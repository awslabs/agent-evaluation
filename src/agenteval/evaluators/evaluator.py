# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
from typing import Optional

from agenteval.conversation_handler import ConversationHandler
from agenteval.hook import Hook
from agenteval.targets import BaseTarget
from agenteval.test import Test
from agenteval.test_result import TestResult
from agenteval.trace_handler import TraceHandler
from agenteval.utils import import_class


class BaseEvaluator(ABC):
    """The `BaseEvaluator` abstract base class defines the common interface for evaluator
    classes.

    Attributes:
        test (Test): The test case.
        target (BaseTarget): The target agent being evaluated.
        conversation (ConversationHandler): Conversation handler for capturing the interaction
            between the evaluator (user) and target (agent).
        trace (TraceHandler): Trace handler for capturing steps during evaluation.
        test_result (TestResult): The result of the test which is set in `BaseEvaluator.run`.
    """

    def __init__(self, test: Test, target: BaseTarget, work_dir: str):
        """Initialize the evaluator instance for a given `Test` and `Target`.

        Args:
            test (Test): The test case.
            target (BaseTarget): The target agent being evaluated.
            work_dir (str): The work directory.
        """
        self.test = test
        self.target = target
        self.conversation = ConversationHandler()
        self.trace = TraceHandler(work_dir=work_dir, test_name=test.name)
        self.test_result = None

    @abstractmethod
    def evaluate(self) -> TestResult:
        """Conduct a test.

        Returns:
            TestResult: The result of the test.
        """
        pass

    def _get_hook_cls(self, hook: Optional[str]) -> Optional[type[Hook]]:
        if hook:
            hook_cls = import_class(hook, parent_class=Hook)
            return hook_cls

    def run(self) -> TestResult:
        """
        Run the evaluator within a trace context manager and run hooks
        if provided.
        """

        hook_cls = self._get_hook_cls(self.test.hook)

        with self.trace:
            if hook_cls:
                hook_cls.pre_evaluate(self.test, self.trace)
            self.test_result = self.evaluate()
            if hook_cls:
                hook_cls.post_evaluate(self.test, self.test_result, self.trace)

        return self.test_result
