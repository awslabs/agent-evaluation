from src.agenteval import summary
import os
from datetime import datetime


def test_create_markdown_summary(mocker):
    mock_get_template = mocker.patch.object(summary.jinja_env, "get_template")
    mock_render = mocker.patch.object(mock_get_template.return_value, "render")
    mock_write_summary = mocker.patch.object(summary, "_write_summary")

    run_start_time = datetime.now()
    run_end_time = datetime.now()

    summary.create_markdown_summary(
        "test-dir", "test-run-id", 100.0, 100, run_start_time, run_end_time, 1000, 300, []
    )

    mock_get_template.assert_called_once_with(
        os.path.join(summary._TEMPLATE_ROOT, summary._TEMPLATE_FILE_NAME)
    )
    mock_render.assert_called_once_with(
        tests=[],
        run_id="test-run-id",
        run_start_time=run_start_time.strftime(summary._TIMESTAMP_FORMAT),
        run_end_time=run_end_time.strftime(summary._TIMESTAMP_FORMAT),
        num_tests=100,
        pass_rate=100.0,
        evaluator_input_token_count=1000,
        evaluator_output_token_count=300,
    )
    mock_write_summary.assert_called_once_with(
        os.path.join("test-dir", os.path.splitext(summary._TEMPLATE_FILE_NAME)[0]),
        mock_render.return_value,
    )
