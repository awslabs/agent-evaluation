import pytest
from agenteval.test import test_suite

test_config = {
    "test_1": {
        "steps": ["step 1, step 2, step 3"],
        "expected_results": ["result 1", "result 2"],
    },
    "test_2": {
        "steps": ["step 1"],
        "expected_results": ["result 1"],
        "max_turns": 5,
    },
    "test_3": {
        "steps": ["step 1"],
        "expected_results": ["result 1"],
    },
}


class TestTestSuite:
    def test_load(self):
        suite = test_suite.TestSuite.load(test_config, None)
        assert suite.num_tests == 3
        assert suite.tests[0].max_turns == test_suite.defaults.MAX_TURNS
        assert suite.tests[1].max_turns == 5

    def test_load_with_filter(self):
        suite = test_suite.TestSuite.load(test_config, filter="test_2,test_3")
        assert suite.num_tests == 2

    @pytest.mark.parametrize(
        "input,expected",
        [
            ("test_1", ["test_1"]),
            ("test_1,test_2", ["test_1", "test_2"]),
            ("test_1, test_2 ", ["test_1", "test_2"]),
        ],
    )
    def test_parse_filter_test_names(self, input, expected):
        assert expected == test_suite.TestSuite._parse_filter(input)
