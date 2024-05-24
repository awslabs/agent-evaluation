# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from agenteval.test import Expected, TestResult


class Test(BaseModel, validate_assignment=True, arbitrary_types_allowed=True):
    """A test case.

    Attributes:
        name: Name of the test.
        steps: List of step to perform for the test.
        expected: The expected results for the test.
        initial_prompt: The initial prompt.
        max_turns: Maximum number of turns allowed for the test.
        hook: The module path to an evaluation hook.
        test_result: The test result.
        start_time: The start time of the test.
        end_time: The end time of the test.
    """

    # do not collect as a pytest
    __test__ = False

    name: str
    steps: list[str]
    expected: Expected
    initial_prompt: Optional[str] = None
    max_turns: int
    hook: Optional[str] = None
    test_result: Optional[TestResult] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
