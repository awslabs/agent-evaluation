import uuid

import pytest

from src.agenteval.targets.aws import bedrock_agent_target
from src.agenteval.utils import aws


@pytest.fixture
def bedrock_agent_fixture(mocker):
    mocker.patch.object(aws.boto3, "Session")

    fixture = bedrock_agent_target.BedrockAgentTarget(
        bedrock_agent_id="test-agent-id",
        bedrock_agent_alias_id="test-alias-id",
        aws_profile="test-profile",
        aws_region="us-west-2",
    )

    return fixture


class TestBedrockAgentTarget:
    def test_session_id(self, bedrock_agent_fixture):
        try:
            uuid.UUID(bedrock_agent_fixture._session_id)
            assert True
        except ValueError:
            assert False

    def test_invoke(self, mocker, bedrock_agent_fixture):
        mock_invoke_agent = mocker.patch.object(
            bedrock_agent_fixture.boto3_client, "invoke_agent"
        )

        mock_invoke_agent.return_value = {
            "completion": [
                {"chunk": {"bytes": b"test "}},
                {
                    "chunk": {
                        "bytes": b"completion",
                    },
                    "trace": {"trace": {"preProcessingTrace": None}},
                },
            ]
        }

        response = bedrock_agent_fixture.invoke("test prompt")

        assert response.response == "test completion"
        assert response.data == {"bedrock_agent_trace": [{"preProcessingTrace": None}]}
