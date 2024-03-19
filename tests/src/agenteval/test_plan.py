import os

from src.agenteval import plan
from src.agenteval.targets import target
import pytest


@pytest.fixture
def plan_fixture():
    return plan.Plan(
        evaluator_config=plan.EvaluatorConfig(type="bedrock-claude"),
        target_config=plan.TargetConfig(
            type="bedrock-agent",
            bedrock_agent_id="test-agent-id",
            bedrock_agent_alias_id="test-alias-id",
        ),
        tasks=[
            plan.Task(
                name="TestTask",
                steps=["step 1", "step 2"],
                expected_results=["result 1"],
                max_turns=2,
            )
        ],
    )


@pytest.fixture
def plan_with_custom_target_fixture():
    return plan.Plan(
        evaluator_config=plan.EvaluatorConfig(type="bedrock-claude"),
        target_config=plan.TargetConfig(type="test.path.CustomTarget"),
        tasks=[
            plan.Task(
                name="TestTask",
                steps=["step 1", "step 2"],
                expected_results=["result 1"],
                max_turns=2,
            )
        ],
    )


class CustomTarget(plan.BaseTarget):
    test_attribute: str

    def invoke(self, prompt):
        return "test response"


class TestPlan:
    def test_create_target_aws_type(self, mocker, plan_fixture):
        mock_session = mocker.patch.object(target.boto3, "Session")
        mocker.patch.object(mock_session.return_value, "client")

        target_cls = plan_fixture.create_target()
        assert isinstance(target_cls, plan.BedrockAgentTarget)

    def test_create_target_custom_type(self, mocker, plan_with_custom_target_fixture):
        mock_get_class = mocker.patch.object(
            plan_with_custom_target_fixture, "_get_class"
        )

        mock_get_class.return_value = CustomTarget

        target = plan_with_custom_target_fixture.create_target()

        assert isinstance(target, CustomTarget)

    def test_create_target_not_subclass(self, mocker, plan_with_custom_target_fixture):
        mock_get_class = mocker.patch.object(
            plan_with_custom_target_fixture, "_get_class"
        )

        class InvalidTarget:
            pass

        mock_get_class.return_value = InvalidTarget

        with pytest.raises(TypeError):
            plan_with_custom_target_fixture.create_target()

    def test_get_class(self, mocker, plan_with_custom_target_fixture):
        mock_import_class = mocker.patch.object(
            plan_with_custom_target_fixture, "_import_class"
        )
        mock_import_class.return_value = CustomTarget

        target_cls = plan_with_custom_target_fixture._get_class(
            config=plan_with_custom_target_fixture.target_config,
        )
        assert target_cls == CustomTarget

    def test_load_tasks(self):
        tasks = plan.Plan._load_tasks(
            task_config=[
                {
                    "name": "TestTask1",
                    "steps": ["step 1, step 2, step 3"],
                    "expected_results": ["result 1", "result 2"],
                },
                {
                    "name": "TestTask2",
                    "steps": ["step 1"],
                    "expected_results": ["result 1"],
                    "max_turns": 5,
                },
            ]
        )

        assert len(tasks) == 2
        assert tasks[0].max_turns == plan.defaults.MAX_TURNS
        assert tasks[1].max_turns == 5

    def test_init_plan(self, tmp_path):
        plan.Plan.init_plan(tmp_path)
        assert os.path.exists(os.path.join(tmp_path, plan._PLAN_FILE_NAME))

    def test_init_plan_exists(self, tmp_path):
        plan.Plan.init_plan(tmp_path)

        with pytest.raises(FileExistsError):
            plan.Plan.init_plan(tmp_path)
