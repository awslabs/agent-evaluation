import pytest

from src.agenteval.targets import q_business
from src.agenteval.targets import target


@pytest.fixture
def q_business_fixture(mocker):
    mock_session = mocker.patch.object(target.boto3, "Session")
    mocker.patch.object(mock_session.return_value, "client")

    fixture = q_business.QBusinessTarget(
        q_business_application_id="test-app-id",
        q_business_user_id="test-user-id",
        aws_profile="test-profile",
        aws_region="us-west-2",
    )
    return fixture


class TestQBusinessTarget:
    def test_invoke_new_conversation(self, mocker, q_business_fixture):
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
        assert q_business_fixture._parent_message_id == "test-sys-msg-id"
        assert q_business_fixture._conversation_id == "test-conv-id"

    def test_invoke_existing_conversation(self, mocker, q_business_fixture):
        q_business_fixture._parent_message_id = "test-sys-msg-id"
        q_business_fixture._conversation_id = "test-conv-id"

        mock_chat_sync = mocker.patch.object(
            q_business_fixture.boto3_client, "chat_sync"
        )
        mock_chat_sync.return_value = {
            "systemMessageId": "test-sys-msg-id-2",
            "conversationId": "test-conv-id",
            "systemMessage": "test message 2",
        }

        q_business_fixture.invoke("test prompt")

        mock_chat_sync.assert_called_once_with(
            applicationId=q_business_fixture._q_business_application_id,
            userId=q_business_fixture._q_business_user_id,
            userMessage="test prompt",
            conversationId="test-conv-id",
            parentMessageId="test-sys-msg-id",
        )

        assert q_business_fixture._parent_message_id == "test-sys-msg-id-2"
        assert q_business_fixture._conversation_id == "test-conv-id"
