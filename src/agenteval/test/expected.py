# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel


class Expected(BaseModel):
    """The expected results for a test.

    Attributes:
        conversation: The expected results observed in the conversation between
            the user and agent.
    """

    conversation: list[str]
