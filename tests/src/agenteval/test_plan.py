import os

from src.agenteval import plan
import pytest

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


class TestPlan:
    def test_load_tests(self):
        tests = plan.Plan._load_tests(test_config=test_config, filter=None)

        assert len(tests) == 3
        assert tests[0].max_turns == plan.defaults.MAX_TURNS
        assert tests[1].max_turns == 5

    def test_load_tests_filter(self):
        tests = plan.Plan._load_tests(test_config=test_config, filter="test_2,test_3")
        assert len(tests) == 2

    @pytest.mark.parametrize(
        "input,expected",
        [
            ("test_1", ["test_1"]),
            ("test_1,test_2", ["test_1", "test_2"]),
            ("test_1, test_2 ", ["test_1", "test_2"]),
        ],
    )
    def test_parse_filter_test_names(self, input, expected):
        assert expected == plan.Plan._parse_filter(input)

    def test_init_plan(self, tmp_path):
        plan.Plan.init_plan(tmp_path)
        assert os.path.exists(os.path.join(tmp_path, plan._PLAN_FILE_NAME))

    def test_init_plan_exists(self, tmp_path):
        plan.Plan.init_plan(tmp_path)

        with pytest.raises(FileExistsError):
            plan.Plan.init_plan(tmp_path)
