import pytest
from src.agenteval.targets.lexv2 import target
from src.agenteval.utils import aws

from io import BytesIO


@pytest.fixture
def lexv2_endpoint_fixture(mocker):
    mocker.patch.object(aws.boto3, "Session")

    fixture = target.LexV2Target()

    return fixture


class TestLexV2Target:

