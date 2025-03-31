from agenteval.evaluators.canonical.evaluator import CanonicalEvaluator
from agenteval.evaluators.model_config.bedrock_model_config import BedrockModelConfig
from src.agenteval.evaluators import evaluator_factory
import pytest
import os

MOCK_MODEL_ID = "12345"
MOCK_REQUEST_BODY = {"max_tokens": 10}

@pytest.fixture
def target_factory_fixture():
    return evaluator_factory.EvaluatorFactory(
        config={"model": "claude-3", "eval_method": "canonical", "aws_region": "us-west-2"}
    )

@pytest.fixture
def target_factory_custom_config_fixture():
    return evaluator_factory.EvaluatorFactory(
        config={"custom_config": {"model_id": "12345", "request_body": {"max_tokens": 10}}, "aws_region": "us-west-2"}
    )

EXPECTED_CUSTOM_MODEL_CONFIG = BedrockModelConfig(
    model_id=MOCK_MODEL_ID,
    request_body=MOCK_REQUEST_BODY
)

class TestEvaluatorFactory:
    @pytest.mark.parametrize("factory_fixture, expected_model_config", [
        ("target_factory_fixture", evaluator_factory.DEFAULT_CLAUDE_3_MODEL_CONFIG),
        ("target_factory_custom_config_fixture", EXPECTED_CUSTOM_MODEL_CONFIG)
    ])
    def test_create(self, mocker, request, factory_fixture, expected_model_config):
        factory = request.getfixturevalue(factory_fixture)
        mock_get_evaluator_class = mocker.patch.object(
            factory, "_get_evaluator_class"
        )

        mock_evaluator_cls = mocker.patch.object(
            evaluator_factory, evaluator_factory._EVALUATOR_METHOD_MAP["canonical"].__name__
        )
        mock_get_evaluator_class.return_value = mock_evaluator_cls

        test = mocker.MagicMock()
        target = mocker.MagicMock()
        work_dir = os.getcwd()

        factory.create(test, target, work_dir)

        mock_evaluator_cls.assert_called_once_with(
            test=test, target=target, work_dir=work_dir, aws_region="us-west-2", model_config=expected_model_config
        )

    def test_get_evaluator_class_works_as_expected(self, target_factory_fixture, target_factory_custom_config_fixture):
        broken_config = evaluator_factory.EvaluatorFactory(
            config={"model": "claude-3", "eval_method": "canoncial", "aws_region": "us-west-2"}
        )

        # Call the actual _get_evaluator_class method
        evaluator_class = target_factory_fixture._get_evaluator_class()
        evaluator_class_custom = target_factory_custom_config_fixture._get_evaluator_class()

        assert evaluator_class == CanonicalEvaluator
        assert evaluator_class_custom == CanonicalEvaluator

        with pytest.raises(KeyError):
            broken_config._get_evaluator_class()
