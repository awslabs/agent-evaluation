from src.agenteval.targets import target
import pytest


class DummyAWSTarget(target.AWSTarget):
    def invoke(self):
        pass


@pytest.fixture
def aws_target_fixture(mocker):
    mock_session = mocker.patch.object(target.boto3, "Session")
    mocker.patch.object(mock_session.return_value, "client")

    return DummyAWSTarget(
        boto3_service_name="test-service-name",
        aws_profile="test-profile",
        aws_region="us-west-2",
        endpoint_url=None,
    )


class TestAWSTarget:
    def test_create_runtime_client(self, mocker, aws_target_fixture):
        mock_session = mocker.patch.object(target.boto3, "Session")
        mock_client = mocker.patch.object(mock_session.return_value, "client")

        aws_target_fixture._create_boto3_client(
            boto3_service_name="test-service-name",
            aws_profile="test-profile",
            aws_region="us-west-2",
            endpoint_url=None,
        )

        mock_session.assert_called_once_with(
            profile_name="test-profile", region_name="us-west-2"
        )

        mock_client.assert_called_once_with(
            "test-service-name", endpoint_url=None
        )
