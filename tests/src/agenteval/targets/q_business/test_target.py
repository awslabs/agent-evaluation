import pytest

from src.agenteval.targets.q_business import target
from src.agenteval.utils import aws


@pytest.fixture
def q_business_fixture(mocker):
    mocker.patch.object(aws.boto3, "Session")

    fixture = target.QBusinessTarget(
        q_business_application_id="test-app-id", q_business_user_id="test-user-id"
    )
    return fixture


class TestQBusinessTarget:
    def test_invoke(self, mocker, q_business_fixture):
        mock_chat_sync = mocker.patch.object(
            q_business_fixture.boto3_client, "chat_sync"
        )
        mock_chat_sync.return_value = {
            "systemMessageId": "test-sys-msg-id",
            "conversationId": "test-conv-id",
            "systemMessage": "test message",
        }

        response = q_business_fixture.invoke("test prompt")

        assert response.response == "test message"
        assert q_business_fixture._chat_sync_args["conversationId"] == "test-conv-id"
        assert q_business_fixture._chat_sync_args["parentMessageId"] == "test-sys-msg-id"
