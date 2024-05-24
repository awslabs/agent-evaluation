# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime

from pydantic import BaseModel

from agenteval.test import Test


class Run(BaseModel):
    """An execution of a test plan."""

    start_time: datetime
    end_time: datetime
    tests: list[Test]
