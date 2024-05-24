# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ListRuns(BaseModel):
    """Return type for BaseStore.list_runs"""

    class Run(BaseModel):
        id: int
        start_time: datetime
        end_time: datetime

    runs: list[Run]


class ListTests(BaseModel):
    """Return type for BaseStore.list_tests"""

    class Test(BaseModel):
        name: str
        start_time: datetime
        end_time: datetime

    tests: list[Test]


class DescribeRun(BaseModel):
    """Return type for BaseStore.describe_run"""

    id: int
    start_time: datetime
    end_time: datetime
    num_tests: int
    pass_rate: float
    evaluator_input_token_count: int
    evaluator_output_token_count: int


class DescribeTest(BaseModel):
    """Return type for BaseStore.describe_test"""

    class Expected(BaseModel):
        conversation: list[str]

    class TestResult(BaseModel):
        result: str
        reasoning: str
        passed: bool
        messages: list[tuple]
        events: list[dict]
        evaluator_input_token_count: int
        evaluator_output_token_count: int

    name: str
    start_time: datetime
    end_time: datetime
    steps: list[str]
    expected: Expected
    initial_prompt: Optional[str]
    max_turns: int
    hook: Optional[str]
    test_result: TestResult
