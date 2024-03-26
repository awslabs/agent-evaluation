import logging
from typing import Optional

import click

from agenteval.plan import Plan
from agenteval.runner import Runner

logger = logging.getLogger(__name__)


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
def run(
    plan_dir: Optional[str],
    verbose: bool,
    num_threads: Optional[int],
):
    plan = Plan.load(plan_dir)
    runner = Runner(
        plan,
        verbose,
        num_threads,
    )
    runner.run()
