# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os

from agenteval import jinja_env
from agenteval.metrics import calculate_pass_rate_metric
from agenteval.test import Test, TestResult

_TEMPLATE_ROOT = "summary"
_TEMPLATE_FILE_NAME = "agenteval_summary.md.jinja"


def create_markdown_summary(
    work_dir: str,
    pass_count: int,
    num_tests: int,
    tests: list[Test],
    test_results: list[TestResult],
):
    """
    Create a Markdown summary of the test results.

    This function uses a Jinja2 template to render a Markdown summary of the
    provided tests and test results.

    The summary is then written to a file in the specified working directory.

    Args:
        work_dir (str): The directory where the summary file will be created.
        pass_count (int): The number of tests that passed.
        num_tests (int): The total number of tests.
        tests (list[Test]): A list of tests.
        test_results (list[TestResult]): A list of test results.

    Returns:
        None
    """
    template = jinja_env.get_template(os.path.join(_TEMPLATE_ROOT, _TEMPLATE_FILE_NAME))
    summary_path = os.path.join(work_dir, os.path.splitext(_TEMPLATE_FILE_NAME)[0])

    metrics = {"pass_rate": calculate_pass_rate_metric(pass_count, num_tests)}

    rendered = template.render(
        tests=tests, results=test_results, zip=zip, metrics=metrics
    )

    _write_summary(summary_path, rendered)


def _write_summary(path: str, summary: str):
    with open(path, "w+") as f:
        f.write(summary)
