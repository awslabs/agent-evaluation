# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from agenteval.test import Test


class Hook:
    """An evaluation hook."""

    def pre_evaluate(test: Test) -> None:
        """
        Method called before evaluation. Can be used to perform any setup tasks.

        Args:
            test (Test): The test case.
        """
        pass

    def post_evaluate(test: Test) -> None:
        """
        Method called after evaluation. This may be used to perform integration testing
        or clean up tasks.

        Args:
            test (Test): The test case.
        """
        pass
