# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid

import pytest
from src.agenteval.targets.lexv2 import target
from src.agenteval.utils import aws


@pytest.fixture
def lexv2_fixture(mocker):
    mocker.patch.object(aws.boto3, "Session")

    fixture = target.LexV2Target(
        bot_id="test-bot-id",
        bot_alias_id="test-alias-id",
        locale_id="test-locale-id",
        aws_profile="test-profile",
        aws_region="us-west-2",
    )

    return fixture


class TestLexV2Target:
    def test_session_id(self, lexv2_fixture):
        try:
            uuid.UUID(lexv2_fixture._session_id)
            assert True
        except ValueError:
            assert False

    def test_invoke_closed(self, mocker, lexv2_fixture):
        mock_recognize_text = mocker.patch.object(
            lexv2_fixture.boto3_client, "recognize_text"
        )
        mock_recognize_text.return_value = {
            "sessionState": {"dialogAction": {"type": "Close"}}
        }

        response = lexv2_fixture.invoke("test prompt")

        assert mock_recognize_text.call_count == 1
        assert response.response == "Completed"

    def test_invoke_opened(self, mocker, lexv2_fixture):
        mock_recognize_text = mocker.patch.object(
            lexv2_fixture.boto3_client, "recognize_text"
        )
        mock_recognize_text.return_value = {
            "sessionState": {"dialogAction": {"type": "None"}},
            "messages": [{"content": "test message"}],
        }

        response = lexv2_fixture.invoke("test prompt")

        assert mock_recognize_text.call_count == 1
        assert response.response == "test message"
