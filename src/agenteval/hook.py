from typing import Optional

from agenteval.test import Test
from agenteval.test_result import TestResult


class Hook:
    """An evaluation hook"""

    def pre_eval(self) -> None:
        """
        Method called before evaluation. Can be used to perform any setup tasks.
        """
        pass

    def post_eval(self, test: Test, test_result: TestResult) -> Optional[TestResult]:
        """
        Method called after evaluation. This may be used to perform integration testing
        or clean up tasks.

        Args:
            test: The test case.
            test_result: The result of the test.

        Returns:
            A TestResult object which overrides the original test result. If None,
            the original test result will be used.
        """
        pass
