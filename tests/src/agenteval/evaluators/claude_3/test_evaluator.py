import io

import pytest

from src.agenteval.evaluators.claude_3 import evaluator
from src.agenteval.utils import aws
from src.agenteval.test import test


@pytest.fixture
def test_fixture():
    return test.Test(
        name="my_test",
        steps=["step 1", "step 2"],
        expected=test.Expected(conversation=["result 1"]),
        initial_prompt="test prompt",
        max_turns=2,
    )


@pytest.fixture
def target_fixture(mocker):
    return mocker.MagicMock()


@pytest.fixture
def evaluator_fixture(mocker, test_fixture, target_fixture):
    mock_session = mocker.patch.object(aws.boto3, "Session")
    mocker.patch.object(mock_session.return_value, "client")

    fixture = evaluator.Claude3Evaluator(
        aws_profile="test-profile",
        aws_region="us-west-2",
        endpoint_url=None,
        test=test_fixture,
        target=target_fixture,
    )

    return fixture


class TestClaude3:
    @pytest.mark.parametrize(
        "xml_data,element_names,expected",
        [
            ("<response>test response</response>", ["response"], ("test response",)),
            ("<response>test response</response>", ["test1", "test2"], (None, None)),
            (
                "<response>test response</response>\n<thinking>test reasoning</thinking>",
                ["response", "thinking"],
                ("test response", "test reasoning"),
            ),
            (
                "<response>test response</response><thinking>test reasoning</thinking>",
                ["response", "thinking"],
                ("test response", "test reasoning"),
            ),
        ],
    )
    def test_extract_content_from_xml(
        self, evaluator_fixture, xml_data, element_names, expected
    ):
        result = evaluator_fixture._extract_content_from_xml(xml_data, element_names)
        assert expected == result

    def test_generate(self, mocker, evaluator_fixture):
        mock_invoke_model = mocker.patch.object(evaluator_fixture, "invoke_model")

        mock_invoke_model.return_value = {
            "body": io.BytesIO(
                b'{"content": [{"text": "<test_element_name>test output/test_element_name> <thinking>test reasoning</thinking>"}]}'
            )
        }

        mock_extract_content_from_xml = mocker.patch.object(
            evaluator_fixture, "_extract_content_from_xml"
        )
        mock_extract_content_from_xml.return_value = "test output", "test reasoning"

        request_body = evaluator.model_configs.REQUEST_BODY
        request_body["system"] = "test system prompt"
        request_body["messages"][0]["content"][0]["text"] = "test prompt"

        result = evaluator_fixture._generate(
            "test system prompt", "test prompt", "test_element_name"
        )

        assert result == ("test output", "test reasoning")

        mock_invoke_model.assert_called_once_with(request_body=request_body)
        mock_extract_content_from_xml.assert_called_once_with(
            "<test_element_name>test output/test_element_name> <thinking>test reasoning</thinking>",
            ["test_element_name", "thinking"],
        )

    def test_run_single_turn_pass(self, mocker, evaluator_fixture):
        mocker.patch.object(evaluator_fixture, "_invoke_target")

        mock_generate_test_status = mocker.patch.object(
            evaluator_fixture, "_generate_test_status"
        )
        mock_generate_test_status.return_value = (
            evaluator.TestStatusCategories.ALL_STEPS_ATTEMPTED.value
        )

        mock_generate_evaluation = mocker.patch.object(
            evaluator_fixture, "_generate_evaluation"
        )
        mock_generate_evaluation.return_value = (
            evaluator.EvaluationCategories.ALL_EXPECTED_RESULTS_OBSERVED.value,
            "",
        )

        evaluator_fixture.evaluate()

        assert evaluator_fixture.test.test_result.passed is True

    def test_run_single_turn_initial_prompt_pass(self, mocker, evaluator_fixture):
        evaluator_fixture.test.initial_prompt = None

        mock_generate_initial_prompt = mocker.patch.object(
            evaluator_fixture, "_generate_initial_prompt"
        )
        mock_generate_initial_prompt.return_value = "test generated prompt"

        mocker.patch.object(evaluator_fixture, "_invoke_target")

        mock_generate_test_status = mocker.patch.object(
            evaluator_fixture, "_generate_test_status"
        )
        mock_generate_test_status.return_value = (
            evaluator.TestStatusCategories.ALL_STEPS_ATTEMPTED.value
        )

        mock_generate_evaluation = mocker.patch.object(
            evaluator_fixture, "_generate_evaluation"
        )
        mock_generate_evaluation.return_value = (
            evaluator.EvaluationCategories.ALL_EXPECTED_RESULTS_OBSERVED.value,
            "",
        )

        evaluator_fixture.evaluate()

        assert evaluator_fixture.test.test_result.passed is True
        assert mock_generate_initial_prompt.call_count == 1

    def test_run_multi_turn_pass(self, mocker, evaluator_fixture):
        mocker.patch.object(evaluator_fixture, "_invoke_target")

        mock_generate_user_response = mocker.patch.object(
            evaluator_fixture, "_generate_user_response"
        )
        mock_generate_user_response.return_value = "test user response"

        mock_generate_test_status = mocker.patch.object(
            evaluator_fixture, "_generate_test_status"
        )
        mock_generate_test_status.side_effect = [
            evaluator.TestStatusCategories.NOT_ALL_STEPS_ATTEMPTED.value,
            evaluator.TestStatusCategories.ALL_STEPS_ATTEMPTED.value,
        ]

        mock_generate_evaluation = mocker.patch.object(
            evaluator_fixture, "_generate_evaluation"
        )
        mock_generate_evaluation.return_value = (
            evaluator.EvaluationCategories.ALL_EXPECTED_RESULTS_OBSERVED.value,
            "",
        )

        evaluator_fixture.evaluate()

        assert evaluator_fixture.test.test_result.passed is True
        assert mock_generate_test_status.call_count == 2
        assert mock_generate_user_response.call_count == 1

    def test_run_max_turns_exceeded(self, mocker, evaluator_fixture):
        mocker.patch.object(evaluator_fixture, "_invoke_target")

        mock_generate_test_status = mocker.patch.object(
            evaluator_fixture, "_generate_test_status"
        )
        mock_generate_test_status.side_effect = [
            evaluator.TestStatusCategories.NOT_ALL_STEPS_ATTEMPTED.value,
            evaluator.TestStatusCategories.NOT_ALL_STEPS_ATTEMPTED.value,
        ]

        mock_generate_user_response = mocker.patch.object(
            evaluator_fixture, "_generate_user_response"
        )
        mock_generate_user_response.return_value = "test user response"

        evaluator_fixture.evaluate()

        assert evaluator_fixture.test.test_result.passed is False
        assert mock_generate_user_response.call_count == 1
