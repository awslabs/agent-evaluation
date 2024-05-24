# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import inspect
from datetime import datetime, timezone
from typing import Optional


class Trace:
    """Captures the events during evaluation for a test.

    Attributes:
        events (list[dict]): A list of events recorded for the test.
    """

    def __init__(self):
        """
        Initialize the trace for a test.
        """
        self.events = []

    def add_event(
        self,
        data: dict,
        name: Optional[str] = None,
        timestamp: datetime = None,
    ):
        """Add an event to the trace.

        Args:
            data (dict): The data to be recorded.
            name (Optional[str]): The name of the event. Defaults to
                the name of the caller function.
            timestamp (datetime.datetime): The timestamp of the event.
                Defaults to the current time.
        """
        event = {
            "name": name or inspect.stack()[1].function,
            "timestamp": timestamp or datetime.now(timezone.utc),
            "data": data,
        }
        self.events.append(event)
