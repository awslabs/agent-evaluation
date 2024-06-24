# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


class NoRecordFoundError(Exception):
    """An exception raised when record cannot be found in the backend store."""

    def __init__(self):
        self.message = "Record not found."
        super().__init__(self.message)


class SchemaOutdatedError(Exception):
    """An exception raised when the backend store's database schema is outdated."""

    def __init__(self, current_revision: str, head_revision: str):
        self.message = (
            "Detected out-of-date database schema "
            f"(found version {current_revision} but expected {head_revision}). "
            "Take a backup of your database, then run `agenteval store upgrade`."
        )
        super().__init__(self.message)


class SchemaAlreadyUpToDateError(Exception):
    """An exception raised on an attempt to upgrade the backend store's database schema
    when it is already up-to-date.
    """

    def __init__(self):
        self.message = "Schema is already up-to-date."
        super().__init__(self.message)
