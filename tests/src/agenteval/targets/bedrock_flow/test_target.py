import pytest

from src.agenteval.targets.bedrock_flow import target
from src.agenteval.utils import aws


@pytest.fixture
def bedrock_flow_fixture(mocker):
    mocker.patch.object(aws.boto3, "Session")

    fixture = target.BedrockFlowTarget(
        bedrock_flow_id="test-agent-id",
        bedrock_flow_alias_id="test-alias-id",
        aws_profile="test-profile",
        aws_region="us-west-2",
    )

    return fixture


class TestBedrockFlowTarget:

    def test_invoke(self, mocker, bedrock_flow_fixture):
        mock_invoke_flow = mocker.patch.object(
            bedrock_flow_fixture.boto3_client, "invoke_flow"
        )

        mock_invoke_flow.return_value = {
            "responseStream": [
                {
                    "flowTraceEvent": {
                        "trace": {"fascinating": "trace content"},
                    },
                },
                {
                    "flowOutputEvent": {
                        "content": {"document": "Meow!"},
                        "nodeType": "FlowOutputNode",
                    },
                },
                {
                    "flowTraceEvent": {
                        "trace": {"some garbage": "or other"},
                    },
                },
                {
                    "flowCompletionEvent": {
                        "completionReason": "SUCCESS",
                    },
                },
            ]
        }

        response = bedrock_flow_fixture.invoke("test prompt")

        assert response.response == "Meow!"
        assert response.data == {
            "bedrock_flow_trace": [
                {"fascinating": "trace content"},
                {"some garbage": "or other"},
            ],
        }
