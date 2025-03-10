import yaml
from click.testing import CliRunner

from src.agenteval import cli
from src.agenteval.plan.plan import _DEFAULT_PLAN_FILE_NAME
from src.agenteval.plan.exceptions import TestFailureError

runner = CliRunner()


def test_init():
    with runner.isolated_filesystem():
        result = runner.invoke(cli.cli, ["init"])
        assert result.exit_code == 0


def test_init_file_exists():
    with runner.isolated_filesystem():
        with open(_DEFAULT_PLAN_FILE_NAME, "w") as stream:
            yaml.safe_dump({}, stream)
        result = runner.invoke(cli.cli, ["init"])
        assert result.exit_code == cli.ExitCode.PLAN_ALREADY_EXISTS.value


def test_run(mocker):
    mock_plan = mocker.patch.object(cli.Plan, "load")

    mock_run = mocker.patch.object(mock_plan.return_value, "run")

    result = runner.invoke(cli.cli, ["run"])

    mock_run.assert_called_once_with(
        verbose=False, num_threads=None, work_dir=None, filter=None
    )
    assert result.exit_code == 0


def test_run_tests_failed(mocker):
    mock_plan = mocker.patch.object(cli.Plan, "load")
    mock_run = mocker.patch.object(mock_plan.return_value, "run")
    mock_run.side_effect = [TestFailureError]

    result = runner.invoke(cli.cli, ["run"])
    assert result.exit_code == cli.ExitCode.TESTS_FAILED.value
