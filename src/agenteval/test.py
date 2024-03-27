from typing import Optional

from pydantic import BaseModel


class Test(BaseModel, validate_assignment=True):
    """A test case for an agent.

    Attributes:
        name: Name of the test
        steps: List of step to perform for the test
        expected_results: List of expected results for the test
        initial_prompt: Optional initial prompt
        max_turns: Maximum number of turns allowed for the test
    """

    # do not collect as a test
    __test__ = False

    name: str
    steps: list[str]
    expected_results: list[str]
    initial_prompt: Optional[str] = None
    max_turns: int