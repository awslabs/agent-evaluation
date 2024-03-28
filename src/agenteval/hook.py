from agenteval.test import Test
from agenteval.test_result import TestResult
from agenteval.trace_handler import TraceHandler


class Hook:
    """An evaluation hook."""

    def pre_evaluate(test: Test, trace: TraceHandler) -> None:
        """
        Method called before evaluation. Can be used to perform any setup tasks.

        Args:
            test (Test): The test case.
            trace (TraceHandler): Trace handler for capturing steps during evaluation.
        """
        pass

    def post_evaluate(test: Test, test_result: TestResult, trace: TraceHandler) -> None:
        """
        Method called after evaluation. This may be used to perform integration testing
        or clean up tasks.

        Args:
            test (Test): The test case.
            test_result (TestResult): The result of the test, which can be overriden
                by updating the attributes of this object.
            trace (TraceHandler): Trace handler for capturing steps during evaluation.
        """
        pass
