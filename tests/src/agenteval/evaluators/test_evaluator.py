from src.agenteval.evaluators import evaluator
import pytest


class DummyAWSEvaluator(evaluator.AWSEvaluator):
    def evaluate(self):
        pass


@pytest.fixture
def aws_evaluator_fixture(mocker):
    mock_session = mocker.patch.object(evaluator.boto3, "Session")
    mocker.patch.object(mock_session.return_value, "client")

    return DummyAWSEvaluator(
        boto3_service_name="test-name",
        test=mocker.MagicMock(),
        target=mocker.MagicMock(),
        work_dir="test-dir",
        aws_profile="test-profile",
        aws_region="us-west-2",
        endpoint_url=None,
    )


class TestAWSEvaluator:
    def test_create_boto3_client(self, mocker, aws_evaluator_fixture):
        mock_session = mocker.patch.object(evaluator.boto3, "Session")
        mock_client = mocker.patch.object(mock_session.return_value, "client")

        aws_evaluator_fixture._create_boto3_client(
            boto3_service_name="test-name",
            aws_profile="test-profile",
            aws_region="us-west-2",
            endpoint_url=None,
        )

        mock_session.assert_called_once_with(
            profile_name="test-profile", region_name="us-west-2"
        )

        mock_client.assert_called_once_with("test-name", endpoint_url=None)
