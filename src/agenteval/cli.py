# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from enum import Enum
from typing import Optional

import click
from rich import print_json

from agenteval.plan import Plan
from agenteval.plan.exceptions import TestFailureError
from agenteval.store import Store
from agenteval.store.db.utils import upgrade_db_schema
from agenteval.store.exceptions import NoRecordFoundError

logger = logging.getLogger(__name__)


class ExitCode(Enum):
    TESTS_FAILED = 1
    PLAN_ALREADY_EXISTS = 2
    NO_RECORD_FOUND = 3


def validate_directory(ctx, param, value):
    if value:
        if not os.path.isdir(value):
            raise click.BadParameter(f"{value} is not a directory")
        if not os.access(value, os.R_OK) or not os.access(value, os.W_OK):
            raise click.BadParameter(f"No read/write permissions for {value}")


@click.group()
def cli():
    pass


@cli.group(help="Retrieve information from the backend store.")
@click.option(
    "--backend-store-url",
    type=str,
    required=False,
    help="The database URL of the backend store. If an URL is not provided, then the environment variable AGENTEVAL_BACKEND_STORE_URL will be used. If the environment variable is not set, then the database URL to the default backend store will be used.",
)
@click.pass_context
def store(
    ctx,
    backend_store_url: Optional[str],
):
    ctx.obj = Store(
        backend_store_url=backend_store_url, init_tables=False, verify_schema=False
    )


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
    "--summary-dir",
    type=str,
    required=False,
    help="The directory to save the test summary to. If a directory is not provided, then the summary will be saved to the current working directory.",
)
@click.option(
    "--backend-store-url",
    type=str,
    required=False,
    help="The database URL of the backend store. If an URL is not provided, then the environment variable AGENTEVAL_BACKEND_STORE_URL will be used. If the environment variable is not set, then the database URL to the default backend store will be used.",
)
def run(
    filter: Optional[str],
    plan_dir: Optional[str],
    verbose: bool,
    num_threads: Optional[int],
    summary_dir: Optional[str],
    backend_store_url: Optional[str],
):
    try:
        plan = Plan.load(plan_dir)
        plan.run(
            verbose=verbose,
            num_threads=num_threads,
            filter=filter,
            summary_dir=summary_dir,
            backend_store_url=backend_store_url,
        )

    except TestFailureError:
        exit(ExitCode.TESTS_FAILED.value)


@store.command(help="List runs in the store.")
@click.option(
    "--max-items",
    type=int,
    required=False,
    default=50,
    help="The maximum number of items to return.",
)
@click.pass_context
def list_runs(ctx, max_items):
    try:
        runs = ctx.obj.list_runs(max_items)
        print_json(runs.model_dump_json())
    except NoRecordFoundError:
        logger.error("[red]No runs found")
        exit(ExitCode.NO_RECORD_FOUND.value)


@store.command(help="List tests from a run in the store.")
@click.option(
    "--run-id",
    type=str,
    required=True,
    help="The run identifier.",
)
@click.option(
    "--max-items",
    type=int,
    required=False,
    default=50,
    help="The maximum number of items to return.",
)
@click.pass_context
def list_tests(ctx, run_id, max_items):
    try:
        tests = ctx.obj.list_tests(run_id, max_items)
        print_json(tests.model_dump_json())
    except NoRecordFoundError:
        logger.error("[red]No runs found")
        exit(ExitCode.NO_RECORD_FOUND.value)


@store.command(help="Describe a run in the store.")
@click.option(
    "--run-id",
    type=str,
    required=True,
    help="The run identifier.",
)
@click.pass_context
def describe_run(ctx, run_id: str):
    try:
        describe_run_response = ctx.obj.describe_run(run_id)
        print_json(describe_run_response.model_dump_json())
    except NoRecordFoundError:
        logger.error("[red]Run not found")
        exit(ExitCode.NO_RECORD_FOUND.value)


@store.command(help="Describe a test in the store.")
@click.option(
    "--test-name",
    type=str,
    required=True,
    help="The name of the test.",
)
@click.option(
    "--run-id",
    type=str,
    required=True,
    help="The run identifier.",
)
@click.pass_context
def describe_test(ctx, test_name: str, run_id: int):
    try:
        test = ctx.obj.describe_test(test_name, run_id)
        print_json(test.model_dump_json())
    except NoRecordFoundError:
        logger.error("[red]Test or run not found")
        exit(ExitCode.NO_RECORD_FOUND.value)


@store.command(help="Upgrade the schema of the backend store.")
@click.pass_context
def upgrade(ctx):
    logger.info("Upgrading schema...")
    upgrade_db_schema(ctx.obj.engine)
