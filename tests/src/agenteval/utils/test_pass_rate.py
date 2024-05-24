from src.agenteval.utils import pass_rate
import pytest


@pytest.mark.parametrize(
    "pass_count,num_tests,expected",
    [(10, 10, 100.0), (0, 10, 0.0), (1, 3, 33.33)],
)
def test_calculate_pass_rate(pass_count, num_tests, expected):
    result = pass_rate.calculate_pass_rate(pass_count, num_tests)
    assert result == expected
