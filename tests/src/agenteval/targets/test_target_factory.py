from src.agenteval.targets import target_factory
import pytest


@pytest.fixture
def target_factory_fixture():
    return target_factory.TargetFactory(
        config={
            "type": "bedrock-agent",
            "bedrock_agent_id": "test-agent-id",
            "bedrock_agent_alias_id": "test-alias-id",
            "aws_region": "us-west-2",
        }
    )


class TestTargetFactory:
    def test_create(sekf, mocker, target_factory_fixture):
        mock_get_target_class = mocker.patch.object(
            target_factory_fixture, "_get_target_class"
        )

        spy_target_cls = mocker.patch.object(
            target_factory, target_factory._TARGET_MAP["bedrock-agent"].__name__
        )
        mock_get_target_class.return_value = spy_target_cls

        target_factory_fixture.create()

        spy_target_cls.assert_called_once_with(
            bedrock_agent_id="test-agent-id",
            bedrock_agent_alias_id="test-alias-id",
            aws_region="us-west-2",
        )

    def test_get_target_class(self, target_factory_fixture):
        cls = target_factory_fixture._get_target_class()

        assert cls == target_factory._TARGET_MAP["bedrock-agent"]

    def test_get_target_class_custom(self, mocker, target_factory_fixture):
        mock_import_class = mocker.patch.object(target_factory, "import_class")

        target_factory_fixture.config["type"] = "custom_target.CustomTarget"

        cls = target_factory_fixture._get_target_class()

        mock_import_class.assert_called_once_with(
            "custom_target.CustomTarget", parent_class=target_factory.BaseTarget
        )

        assert cls == mock_import_class.return_value
