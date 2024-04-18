from src.agenteval.utils import aws


def test_create_boto3_client(mocker):
    mock_config = mocker.patch.object(aws, "Config")
    mock_session = mocker.patch.object(aws.boto3, "Session")
    mock_client = mocker.patch.object(mock_session.return_value, "client")

    aws.create_boto3_client(
        boto3_service_name="test-service-name",
        aws_profile="test-profile",
        aws_region="us-west-2",
        endpoint_url=None,
        max_retry=10,
    )

    mock_config.assert_called_once_with(
        retries={"max_attempts": 10, "mode": aws._RETRY_MODE},
    )

    mock_session.assert_called_once_with(
        profile_name="test-profile", region_name="us-west-2"
    )

    mock_client.assert_called_once_with(
        "test-service-name", endpoint_url=None, config=mock_config.return_value
    )
