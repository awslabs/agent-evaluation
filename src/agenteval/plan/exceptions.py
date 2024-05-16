# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


class TestFailureError(Exception):
    # do not collect as a pytest
    __test__ = False

    def __init__(self, message="One or more tests failed"):
        self.message = message
        super().__init__(self.message)
