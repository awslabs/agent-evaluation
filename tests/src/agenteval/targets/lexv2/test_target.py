import pytest
from src.agenteval.targets.lexv2 import target
from src.agenteval.utils import aws

from io import BytesIO


@pytest.fixture
def lexv2_endpoint_fixture(mocker):
    mocker.patch.object(aws.boto3, "Session")

    fixture = target.LexV2Target(
        bot_id="test-bot-id",
        bot_alias_id="test-alias-id",
        locale_id="test-locale-id",
        session_id="test-session-id",
        aws_profile="test-profile",
        aws_region="us-west-2"
    )

    return fixture


class TestLexV2Target:
`   def test_base_args(self, lexv2_endpoint_fixture):
    assert lexv2_endpoint_fixture. == {

    }
