from typing import Optional

from pydantic import BaseModel


class Task(BaseModel, validate_assignment=True):
    """A test case for an agent.

    Attributes:
        name: Name of the task
        steps: List of step to perform for the task
        expected_results: List of expected results for the task
        initial_prompt: Optional initial prompt
        max_turns: Maximum number of turns allowed for the task
    """

    name: str
    steps: list[str]
    expected_results: list[str]
    initial_prompt: Optional[str] = None
    max_turns: int
