import pytest

from src.agenteval.targets.ag2 import target


@pytest.fixture
def ag2_target_fixture(mocker):
    mocker.patch.object(target, "LLMConfig")
    mocker.patch.object(target, "AssistantAgent")
    mocker.patch.object(target, "UserProxyAgent")

    fixture = target.AG2Target(
        model="gpt-4o-mini",
        api_type="openai",
        api_key="test-api-key",
        system_message="You are a test assistant.",
        max_turns=5,
    )

    return fixture


class TestAG2Target:
    def test_init(self, ag2_target_fixture):
        assert ag2_target_fixture._model == "gpt-4o-mini"
        assert ag2_target_fixture._api_type == "openai"
        assert ag2_target_fixture._api_key == "test-api-key"
        assert ag2_target_fixture._system_message == "You are a test assistant."
        assert ag2_target_fixture._max_turns == 5

    def test_init_defaults(self, mocker):
        mocker.patch.object(target, "LLMConfig")
        mocker.patch.object(target, "AssistantAgent")
        mocker.patch.object(target, "UserProxyAgent")

        fixture = target.AG2Target()

        assert fixture._model == "gpt-4o-mini"
        assert fixture._api_type == "openai"
        assert fixture._system_message == "You are a helpful AI assistant."
        assert fixture._max_turns == 3

    def test_invoke(self, ag2_target_fixture):
        mock_user_proxy = ag2_target_fixture._user_proxy
        mock_result = mock_user_proxy.run.return_value.process.return_value
        mock_result.summary = "Hi there!"

        response = ag2_target_fixture.invoke("Hello")

        assert response.response == "Hi there!"
        mock_user_proxy.run.assert_called_once()

    def test_invoke_empty_summary(self, ag2_target_fixture):
        mock_user_proxy = ag2_target_fixture._user_proxy
        mock_result = mock_user_proxy.run.return_value.process.return_value
        mock_result.summary = ""

        response = ag2_target_fixture.invoke("Hello")

        assert response.response == ""

    def test_invoke_none_result(self, ag2_target_fixture):
        mock_user_proxy = ag2_target_fixture._user_proxy
        mock_user_proxy.run.return_value.process.return_value = None

        response = ag2_target_fixture.invoke("Hello")

        assert response.response == ""

    def test_invoke_resets_agents(self, ag2_target_fixture):
        mock_assistant = ag2_target_fixture._assistant
        mock_user_proxy = ag2_target_fixture._user_proxy
        mock_result = mock_user_proxy.run.return_value.process.return_value
        mock_result.summary = "response"

        ag2_target_fixture.invoke("first prompt")
        ag2_target_fixture.invoke("second prompt")

        assert mock_assistant.reset.call_count == 2
        assert mock_user_proxy.reset.call_count == 2
