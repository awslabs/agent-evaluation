import yaml
from click.testing import CliRunner

from src.agenteval import cli
from src.agenteval.plan import _PLAN_FILE_NAME

runner = CliRunner()


def test_init():
    with runner.isolated_filesystem():
        result = runner.invoke(cli.cli, ["init"])
        assert result.exit_code == 0


def test_init_file_exists():
    with runner.isolated_filesystem():
        with open(_PLAN_FILE_NAME, "w") as stream:
            yaml.safe_dump({}, stream)
        result = runner.invoke(cli.cli, ["init"])
        assert result.exit_code == 1


def test_run(mocker):
    mock_plan = mocker.patch.object(cli.Plan, "load")
    mock_plan.return_value.tests = []

    mock_runner = mocker.patch.object(cli, "Runner")
    mock_runner.return_value.num_failed = 0
    mock_run = mocker.patch.object(mock_runner.return_value, "run")
    mock_run.return_value = 0

    result = runner.invoke(cli.cli, ["run"])

    assert mock_plan.call_count == 1
    mock_runner.assert_called_once_with(
        mock_plan.return_value,
        False,
        None,
        None,
    )
    assert mock_run.call_count == 1
    assert result.exit_code == 0
