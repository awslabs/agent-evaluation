# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from agenteval.test import Test, TestResult
from agenteval.trace import Trace


class Hook:
    """An evaluation hook."""

    def pre_evaluate(test: Test, trace: Trace) -> None:
        """
        Method called before evaluation. Can be used to perform any setup tasks.

        Args:
            test (Test): The test case.
            trace (Trace): Captures steps during evaluation.
        """
        pass

    def post_evaluate(test: Test, test_result: TestResult, trace: Trace) -> None:
        """
        Method called after evaluation. This may be used to perform integration testing
        or clean up tasks.

        Args:
            test (Test): The test case.
            test_result (TestResult): The result of the test, which can be overriden
                by updating the attributes of this object.
            trace (Trace): Captures steps during evaluation.
        """
        pass
