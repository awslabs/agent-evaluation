from src.agenteval.store import store
from src.agenteval.run import Test
from src.agenteval.test.test import TestResult, Expected
import datetime
import pytest


@pytest.fixture
def store_fixture(tmpdir):
    return store.Store(f"sqlite:///{tmpdir}/test.db")


class TestSQLiteStore:
    def test_save_run(self, mocker, store_fixture):
        mock_session = mocker.patch.object(store, "Session")
        mock_run_model = mocker.patch.object(store.models, "Run")
        mock_test_model = mocker.patch.object(store.models, "Test")
        mock_expected_model = mocker.patch.object(store.models, "Expected")
        mock_test_result_model = mocker.patch.object(store.models, "TestResult")
        mock_session_add = mocker.patch.object(
            mock_session.return_value.__enter__.return_value, "add"
        )
        mock_session_commit = mocker.patch.object(
            mock_session.return_value.__enter__.return_value, "commit"
        )

        run_start_time = datetime.datetime.now()
        run_end_time = datetime.datetime.now()
        test_start_time = datetime.datetime.now()
        test_end_time = datetime.datetime.now()
        expected = Expected(conversation=["result 1", "result 2"])
        tests = [
            Test(
                name="test_1",
                steps=["step 1", "step 2"],
                expected=expected,
                max_turns=3,
                start_time=test_start_time,
                end_time=test_end_time,
                test_result=TestResult(
                    result="test result",
                    reasoning="test reasoning",
                    passed=True,
                    messages=[],
                    events=[],
                    evaluator_input_token_count=1000,
                    evaluator_output_token_count=300,
                ),
            )
        ]

        store_fixture.save_run(
            store.Run(
                start_time=run_start_time,
                end_time=run_end_time,
                evaluator_input_token_count=1000,
                evaluator_output_token_count=300,
                tests=tests,
            )
        )

        mock_session.assert_called_once_with(store_fixture.engine)

        mock_run_model.assert_called_once_with(
            start_time=run_start_time,
            end_time=run_end_time,
            tests=[mock_test_model.return_value],
        )

        mock_test_model.assert_called_once_with(
            name="test_1",
            steps=store.json.dumps(["step 1", "step 2"]),
            expected=mock_expected_model.return_value,
            initial_prompt=None,
            max_turns=3,
            hook=None,
            start_time=test_start_time,
            end_time=test_end_time,
            test_result=mock_test_result_model.return_value,
        )

        mock_expected_model.assert_called_once_with(
            conversation=store.json.dumps(["result 1", "result 2"])
        )

        mock_test_result_model.assert_called_once_with(
            result="test result",
            reasoning="test reasoning",
            passed=True,
            messages=store.json.dumps([]),
            events=store.json.dumps([]),
            evaluator_input_token_count=1000,
            evaluator_output_token_count=300,
        )

        mock_session_add.assert_called_once_with(mock_run_model.return_value)
        mock_session_commit.assert_called_once_with()
