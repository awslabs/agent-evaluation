from src.agenteval.evaluators import evaluator_factory
import pytest
import os


@pytest.fixture
def target_factory_fixture():
    return evaluator_factory.EvaluatorFactory(
        config={"model": "claude-3", "aws_region": "us-west-2"}
    )


class TestEvaluatorFactory:
    def test_create(self, mocker, target_factory_fixture):
        mock_get_evaluator_class = mocker.patch.object(
            target_factory_fixture, "_get_evaluator_class"
        )

        mock_evaluator_cls = mocker.patch.object(
            evaluator_factory, evaluator_factory._EVALUATOR_MAP["claude-3"].__name__
        )
        mock_get_evaluator_class.return_value = mock_evaluator_cls

        test = mocker.MagicMock()
        target = mocker.MagicMock()
        work_dir = os.getcwd()

        target_factory_fixture.create(test, target, work_dir)

        mock_evaluator_cls.assert_called_once_with(
            test=test, target=target, work_dir=work_dir, aws_region="us-west-2"
        )
