from src.agenteval import metrics
import pytest


@pytest.mark.parametrize(
    "pass_count,num_tests,expected",
    [
        (10, 10, 100.0),
        (0, 10, 0.0),
        (1, 3, 33.33)
    ],
)
def test_calculate_pass_rate_metric(pass_count, num_tests, expected):
    pass_rate = metrics.calculate_pass_rate_metric(pass_count, num_tests)
    assert pass_rate == expected
