# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


def calculate_pass_rate_metric(pass_count: int, num_tests: int) -> float:
    """Calculate the pass rate metric.

    Args:
        pass_count (int): The number of tests that passed.
        num_tests (int): The total number of tests.

    Returns:
        float: The pass rate metric.
    """
    return round((pass_count / num_tests) * 100, 2)
