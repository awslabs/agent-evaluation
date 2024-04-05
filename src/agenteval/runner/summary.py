import os

from agenteval import jinja_env
from agenteval.test import Test
from agenteval.test_result import TestResult

_MARKDOWN_SUMMARY_TEMPLATE_PATH = "agenteval_summary.md.j2"


def create_markdown_summary(
    work_dir: str, tests: list[Test], test_results: list[TestResult]
) -> str:
    template = jinja_env.get_template(_MARKDOWN_SUMMARY_TEMPLATE_PATH)

    summary_path = os.path.join(
        work_dir, os.path.splitext(_MARKDOWN_SUMMARY_TEMPLATE_PATH)[0]
    )

    rendered = template.render(tests=tests, results=test_results, zip=zip)

    with open(summary_path, "w+") as f:
        f.write(rendered)

    return summary_path
