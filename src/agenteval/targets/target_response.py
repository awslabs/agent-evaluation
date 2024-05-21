# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

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
