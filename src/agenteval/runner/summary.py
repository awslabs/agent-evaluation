import os

from agenteval import jinja_env
from agenteval.task import Task
from agenteval.test_result import TestResult

_MARKDOWN_SUMMARY_TEMPLATE_PATH = "agenteval_summary.md.j2"


def create_markdown_summary(tasks: list[Task], task_results: list[TestResult]) -> str:
    template = jinja_env.get_template(_MARKDOWN_SUMMARY_TEMPLATE_PATH)

    cwd = os.getcwd()
    summary_path = os.path.join(
        cwd, os.path.splitext(_MARKDOWN_SUMMARY_TEMPLATE_PATH)[0]
    )

    rendered = template.render(tasks=tasks, results=task_results, zip=zip)

    with open(summary_path, "w+") as f:
        f.write(rendered)

    return summary_path
