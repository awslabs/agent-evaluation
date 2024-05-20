# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, computed_field, model_validator

from agenteval import defaults
from agenteval.test import Test


class TestSuite(BaseModel):
    """A collection of tests to be executed.

    Attributes:
        tests: A list of tests.
    """

    tests: list[Test]

    # do not collect as a pytest
    __test__ = False

    @model_validator(mode="after")
    def _check_test_names_unique(self) -> TestSuite:
        unique_names = len(set(test.name for test in self.tests))

        if unique_names != len(self.tests):
            raise ValueError("Test names must be unique")

        return self

    def __iter__(self):
        return iter(self.tests)

    @computed_field
    @property
    def num_tests(self) -> int:
        """Returns the number of tests in the test suite."""
        return len(self.tests)

    @classmethod
    def load(cls, config: dict[str, dict], filter: Optional[str]) -> TestSuite:
        """Loads a `TestSuite` from a list of test configurations and an optional filter.

        Args:
            config (dict[str, dict]): A dictionary of test configurations, where
                the keys are the test names and the values are the test cases as dictionaries.
            filter (Optional[str]): A filter string to apply when loading the tests.

        Returns:
            TestSuite: A `TestSuite` instance containing the loaded tests.
        """
        return cls(tests=TestSuite._load_tests(config, filter))

    @staticmethod
    def _load_tests(config: dict[str, dict], filter: Optional[str]) -> list[Test]:
        tests = []

        if filter:
            names = TestSuite._parse_filter(filter)
        else:
            names = config.keys()

        for name in names:
            tests.append(
                Test(
                    name=name,
                    steps=config[name]["steps"],
                    expected_results=config[name]["expected_results"],
                    initial_prompt=config[name].get("initial_prompt"),
                    max_turns=config[name].get("max_turns", defaults.MAX_TURNS),
                    hook=config[name].get("hook"),
                )
            )

        return tests

    @staticmethod
    def _parse_filter(filter: str) -> list[str]:
        return [n.strip() for n in filter.split(",")]
