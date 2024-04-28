import pytest

from src.agenteval.targets.bedrock_knowledge_base import target
from src.agenteval.utils import aws


@pytest.fixture
def bedrock_knowledgebase_fixture(mocker):
    mock_session = mocker.patch.object(aws.boto3, "Session")
    mocker.patch.object(mock_session.return_value, "client")

    fixture = target.BedrockKnowledgeBaseTarget(
        model_id="bedrock-model-id",
        knowledge_base_id="bedrock-knowledge-base-id",
        aws_profile="test-profile",
        aws_region="us-west-2",
    )

    return fixture


class TestBedrockKnowledgebaseTarget:
    _GENERATED_TEXT = "generated text"
    _SESSION_ID = "session-id"

    def test_invoke(self, mocker, bedrock_knowledgebase_fixture):
        mock_knowlegebase_retrieve_and_generate = mocker.patch.object(
            bedrock_knowledgebase_fixture.boto3_client, "retrieve_and_generate"
        )

        mock_knowlegebase_retrieve_and_generate.return_value = {
            "citations": [
                {
                    "generatedResponsePart": {
                        "textResponsePart": {
                            "span": {"end": 10, "start": 0},
                            "text": "generated text from citation 1",
                        }
                    },
                    "retrievedReferences": [
                        {
                            "content": {"text": "referenced text"},
                            "location": {"s3Location": {"uri": "s3://"}, "type": "s3"},
                            "metadata": {"string": None},
                        }
                    ],
                },
                {
                    "generatedResponsePart": {
                        "textResponsePart": {
                            "span": {"end": 20, "start": 10},
                            "text": "generated text from citation 2",
                        }
                    },
                    "retrievedReferences": [
                        {
                            "content": {"text": "referenced text"},
                            "location": {"s3Location": {"uri": "s3://"}, "type": "s3"},
                            "metadata": {"string": None},
                        }
                    ],
                },
            ],
            "output": {"text": self._GENERATED_TEXT},
            "sessionId": self._SESSION_ID,
        }

        response = bedrock_knowledgebase_fixture.invoke("test prompt")

        assert response.response == self._GENERATED_TEXT
        assert bedrock_knowledgebase_fixture._session_id == self._SESSION_ID
        assert len(response.data.get("bedrock_knowledgebase_citations")) == 2
