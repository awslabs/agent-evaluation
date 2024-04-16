# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import inspect
import json
import os
from datetime import datetime, timezone
from typing import Optional

_TRACE_DIR = "agenteval_traces"


class TraceHandler:
    """
    Captures trace data.

    Attributes:
        test_name (str): Name of the test.
        steps (list): List of steps in the trace.
    """

    def __init__(self, test_name: str, work_dir: str):
        """
        Initialize the trace handler.

        Args:
            test_name (str): Name of the trace
        """
        self.test_name = test_name
        self.trace_dir = os.path.join(work_dir, _TRACE_DIR)
        self.start_time = None
        self.end_time = None
        self.steps = []

    def __enter__(self):
        self.start_time = datetime.now(timezone.utc)
        return self

    def __exit__(self, *exc):
        self.end_time = datetime.now(timezone.utc)
        self._dump_trace()

    def _dump_trace(self):
        """Dump the trace to a JSON file."""

        os.makedirs(self.trace_dir, exist_ok=True)

        with open(os.path.join(self.trace_dir, f"{self.test_name}.json"), "w") as f:
            json.dump(self._get_trace(), f, default=str)

    def _get_trace(self) -> str:
        return {
            "test_name": self.test_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "steps": self.steps,
        }

    def add_step(self, step_name: Optional[str] = None, **kwargs):
        """Add a step to the trace.

        Args:
            step_name (str, optional): The name of the step. Defaults to
                the name of the caller function
            **kwargs: Additional data to include in the step
        """
        step_name = step_name or inspect.stack()[1].function
        step = {"timestamp": datetime.now(timezone.utc), "step_name": step_name}
        step.update(kwargs)
        self.steps.append(step)
