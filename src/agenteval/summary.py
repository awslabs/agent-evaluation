# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os

from agenteval import jinja_env
from agenteval.test import Test, TestResult

_TEMPLATE_ROOT = "summary"
_TEMPLATE_FILE_NAME = "agenteval_summary.md.jinja"


def create_markdown_summary(
    work_dir: str, tests: list[Test], test_results: list[TestResult]
):
    template = jinja_env.get_template(os.path.join(_TEMPLATE_ROOT, _TEMPLATE_FILE_NAME))
    summary_path = os.path.join(work_dir, os.path.splitext(_TEMPLATE_FILE_NAME)[0])

    metrics = {"pass_rate": calculate_pass_rate_metric(tests, test_results)}

    rendered = template.render(
        tests=tests, results=test_results, zip=zip, metrics=metrics
    )

    _write_summary(summary_path, rendered)


def calculate_pass_rate_metric(
    tests: list[Test], test_results: list[TestResult]
) -> float:
    pass_rate = 0
    for test, result in zip(tests, test_results):
        if result.success:
            pass_rate += 1
    return (pass_rate / len(tests)) * 100


def _write_summary(path: str, summary: str):
    with open(path, "w+") as f:
        f.write(summary)
