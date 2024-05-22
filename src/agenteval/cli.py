# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os
from enum import Enum
from typing import Optional

import click

from agenteval.plan import Plan
from agenteval.plan.exceptions import TestFailureError


class ExitCode(Enum):
    TESTS_FAILED = 1
    PLAN_ALREADY_EXISTS = 2


def validate_directory(ctx, param, value):
    if value:
        if not os.path.isdir(value):
            raise click.BadParameter(f"{value} is not a directory")
        if not os.access(value, os.R_OK) or not os.access(value, os.W_OK):
            raise click.BadParameter(f"No read/write permissions for {value}")


@click.group()
def cli():
    pass


@cli.command(help="Initialize a test plan.")
@click.option(
    "--plan-dir",
    type=str,
    required=False,
    help="The directory to store the test plan. If a directory is not provided, the test plan will be saved to the current working directory.",
    callback=validate_directory,
)
def init(plan_dir: Optional[str]):
    try:
        Plan.init_plan(plan_dir)
    except FileExistsError:
        exit(ExitCode.PLAN_ALREADY_EXISTS.value)


@cli.command(help="Run test plan.")
@click.option(
    "--filter",
    type=str,
    required=False,
    help="Specifies the test(s) to run, where multiple tests should be seperated using a comma. If a filter is not provided, all tests will be run.",
)
@click.option(
    "--plan-dir",
    type=str,
    required=False,
    help="The directory where the test plan is stored. If a directory is not provided, the test plan will be read from the current working directory.",
    callback=validate_directory,
)
@click.option(
    "--verbose",
    is_flag=True,
    type=bool,
    default=False,
    help="Whether to enable verbose logging. Defaults to False.",
)
@click.option(
    "--num-threads",
    type=int,
    required=False,
    help="Number of threads used to run tests concurrently. If the number of threads is not provided, the thread count will be set to the number of tests (up to a maximum of 45 threads).",
)
@click.option(
    "--work-dir",
    type=str,
    required=False,
    help="The directory where the test result and trace will be generated. If a directory is not provided, the assets will be saved to the current working directory.",
    callback=validate_directory,
)
def run(
    filter: Optional[str],
    plan_dir: Optional[str],
    verbose: bool,
    num_threads: Optional[int],
    work_dir: Optional[str],
):
    try:
        plan = Plan.load(plan_dir)
        plan.run(
            verbose=verbose, num_threads=num_threads, work_dir=work_dir, filter=filter
        )

    except TestFailureError:
        exit(ExitCode.TESTS_FAILED.value)
