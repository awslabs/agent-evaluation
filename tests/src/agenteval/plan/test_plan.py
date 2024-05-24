import os

from src.agenteval.plan import plan
import pytest


config = {
    "evaluator": {"model": "claude-3"},
    "target": {
        "type": "bedrock-agent",
        "bedrock_agent_id": "test-agent-id",
        "bedrock_agent_alias_id": "test-alias-id",
    },
    "tests": {
        "test_1": {
            "steps": ["step 1, step 2, step 3"],
            "expected": {"conversation": ["result 1", "result 2"]},
        },
        "test_2": {
            "steps": ["step 1"],
            "expected": {"conversation": ["result 1"]},
            "max_turns": 5,
        },
        "test_3": {
            "steps": ["step 1"],
            "expected": {"conversation": ["result 1"]},
        },
    },
}


@pytest.fixture
def backend_store_url_fixture(tmpdir):
    return f"sqlite:///{tmpdir}/test.db"


@pytest.fixture
def plan_fixture():
    return plan.Plan(config=config)


class TestPlan:
    def test_load(self, mocker):
        mock_load_yaml = mocker.patch.object(plan.Plan, "_load_yaml")
        mock_load_yaml.return_value = {}

        test_plan = plan.Plan.load(plan_dir=None)

        mock_load_yaml.assert_called_once_with(
            os.path.join(os.getcwd(), plan._PLAN_FILE_NAME)
        )

        assert test_plan.config == {}

    def test_init_plan(self, tmp_path):
        plan.Plan.init_plan(tmp_path)
        assert os.path.exists(os.path.join(tmp_path, plan._PLAN_FILE_NAME))

    def test_init_plan_exists(self, tmp_path):
        plan.Plan.init_plan(tmp_path)

        with pytest.raises(FileExistsError):
            plan.Plan.init_plan(tmp_path)

    @pytest.mark.parametrize(
        "num_tests,num_threads,expected",
        [
            (100, 3, 3),
            (
                plan.defaults.MAX_NUM_THREADS - 1,
                None,
                plan.defaults.MAX_NUM_THREADS - 1,
            ),
            (
                plan.defaults.MAX_NUM_THREADS + 1,
                None,
                plan.defaults.MAX_NUM_THREADS,
            ),
        ],
    )
    def test_resolve_num_threads(self, num_tests, num_threads, expected):
        threads = plan.Plan._resolve_num_threads(
            num_tests=num_tests, num_threads=num_threads
        )
        assert threads == expected

    def test_run(self, mocker, plan_fixture, backend_store_url_fixture):
        spy_setup_run = mocker.spy(plan_fixture, "_setup_run")

        mock_log_run_start = mocker.patch.object(plan, "log_run_start")

        mock_run_concurrent = mocker.patch.object(plan_fixture, "_run_concurrent")
        mock_run_concurrent.side_effect = lambda: setattr(
            plan_fixture, "_pass_count", plan_fixture._num_tests
        )

        mocker.patch.object(plan_fixture, "_save_run")
        mock_log_run_end = mocker.patch.object(plan, "log_run_end")
        mock_create_markdown_summary = mocker.patch.object(
            plan, "create_markdown_summary"
        )

        plan_fixture.run(False, None, None, None, backend_store_url_fixture)

        spy_setup_run.assert_called_once_with(
            None, None, None, backend_store_url_fixture
        )
        mock_log_run_start.assert_called_once()
        mock_run_concurrent.assert_called_once()
        mock_log_run_end.assert_called_once()
        mock_create_markdown_summary.assert_called_once()

    def test_run_failed_test(self, mocker, plan_fixture, backend_store_url_fixture):
        mocker.patch.object(plan, "log_run_start")

        mock_run_concurrent = mocker.patch.object(plan_fixture, "_run_concurrent")
        mock_run_concurrent.side_effect = lambda: setattr(
            plan_fixture, "_pass_count", plan_fixture._num_tests - 1
        )
        mocker.patch.object(plan_fixture, "_save_run")
        mocker.patch.object(plan, "log_run_end")
        mocker.patch.object(plan, "create_markdown_summary")

        with pytest.raises(plan.TestFailureError):
            plan_fixture.run(False, None, None, None, backend_store_url_fixture)

    def test_run_concurrent(self, mocker, plan_fixture, backend_store_url_fixture):
        mock_thread_pool_executor = mocker.patch.object(
            plan.concurrent.futures, "ThreadPoolExecutor"
        )

        mock_submit = mocker.patch.object(
            mock_thread_pool_executor.return_value.__enter__.return_value, "submit"
        )
        mock_as_completed = mocker.patch.object(plan.concurrent.futures, "as_completed")

        plan_fixture._setup_run(None, None, None, backend_store_url_fixture)

        plan_fixture._run_concurrent()

        assert mock_submit.call_count == plan_fixture._num_tests
        mock_as_completed.assert_called_once_with(
            [mock_submit.return_value for _ in range(plan_fixture._num_tests)]
        )
