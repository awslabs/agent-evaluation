from src.agenteval import summary
import os


def test_create_markdown_summary(mocker):
    mock_get_template = mocker.patch.object(summary.jinja_env, "get_template")
    mock_render = mocker.patch.object(mock_get_template.return_value, "render")
    mock_calculate_pass_rate_metric = mocker.patch.object(
        summary, "calculate_pass_rate_metric"
    )
    mock_write_summary = mocker.patch.object(summary, "_write_summary")

    summary.create_markdown_summary("test-work-dir", [], [])

    mock_get_template.assert_called_once_with(
        os.path.join(summary._TEMPLATE_ROOT, summary._TEMPLATE_FILE_NAME)
    )
    mock_render.assert_called_once_with(
        tests=[],
        results=[],
        zip=zip,
        metrics={"pass_rate": mock_calculate_pass_rate_metric.return_value},
    )
    mock_write_summary.assert_called_once_with(
        os.path.join("test-work-dir", os.path.splitext(summary._TEMPLATE_FILE_NAME)[0]),
        mock_render.return_value,
    )
