# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from typing import Optional

import click

from agenteval.plan import Plan
from agenteval.runner import Runner

logger = logging.getLogger(__name__)


def validate_directory(directory):
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"{directory} is not a directory")
    if not os.access(directory, os.R_OK) or not os.access(directory, os.W_OK):
        raise PermissionError(f"No read/write permissions for {directory}")


@click.group()
def cli():
    pass


@cli.command(help="Initialize a test plan.")
@click.option(
    "--plan-dir",
    type=str,
    required=False,
    help="The destination directory for storing the test plan. If unspecified, then the test plan is saved to the current working directory.",
)
def init(plan_dir: Optional[str]):
    if plan_dir:
        validate_directory(plan_dir)
    try:
        path = Plan.init_plan(plan_dir)
        logger.info(f"[green]Test plan created at {path}")

    except FileExistsError as e:
        logger.error(f"[red]{e}")
        exit(1)


@cli.command(help="Run test plan.")
@click.option(
    "--plan-dir",
    type=str,
    required=False,
    help="The directory where the test plan is stored. If unspecified, then the current working directory is used.",
)
@click.option(
    "--verbose",
    is_flag=True,
    type=bool,
    default=False,
    help="Controls the verbosity of the terminal logs.",
)
@click.option(
    "--num-threads",
    type=int,
    required=False,
    help="Number of threads (and thus tests) to run concurrently. If unspecified, number of threads will equal the total number of tests.",
)
@click.option(
    "--work-dir",
    type=str,
    required=False,
    help="The directory where the test result and trace will be generated. If unspecified, then the current working directory is used.",
)
def run(
    plan_dir: Optional[str],
    verbose: bool,
    num_threads: Optional[int],
    work_dir: Optional[str],
):
    try:
        plan = Plan.load(plan_dir)
        if work_dir:
            validate_directory(work_dir)
        runner = Runner(
            plan,
            verbose,
            num_threads,
            work_dir,
        )
        num_failed = runner.run()
        _num_failed_exit(num_failed)

    except Exception as e:
        _exception_exit(e)


def _num_failed_exit(num_failed):
    exit(1 if num_failed else 0)


def _exception_exit(e):
    logger.exception(f"Error running test: {e}")
    exit(1)
