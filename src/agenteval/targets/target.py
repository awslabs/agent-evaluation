# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class TargetResponse(BaseModel):
    """A target's response.

    Attributes:
        response: The response string.
        data: Additional data (if applicable).
    """

    response: str
    data: Optional[dict] = None


class BaseTarget(ABC):
    """The `BaseTarget` abstract base class defines the common interface for target
    classes.
    """

    @abstractmethod
    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt and return a response as a string.

        Args:
            prompt: The prompt string to pass to the target.

        Returns:
            A TargetResponse object containing the target's response string and
            any trace data (if applicable).
        """
        pass
