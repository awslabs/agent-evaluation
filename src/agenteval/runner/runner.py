import concurrent.futures
import logging
import os
import time
from typing import Optional

from rich.progress import Progress

from agenteval.plan import Plan
from agenteval.runner.summary import create_markdown_summary

logger = logging.getLogger(__name__)


class Runner:
    def __init__(
        self,
        plan: Plan,
        verbose: bool,
        num_threads: Optional[int],
        work_dir: Optional[str],
    ):
        self.plan = plan
        self.work_dir = work_dir if work_dir else os.getcwd()
        self.num_tests = len(self.plan.tests)
        self.verbose = verbose
        self.num_threads = num_threads
        if not self.num_threads:
            self.num_threads = self.num_tests
        self.results = {test.name: None for test in self.plan.tests}
        self.num_failed = 0

    def run(self) -> int:
        self._log_run_start()

        self.start_time = time.time()
        with Progress(transient=True) as self.progress:
            self.tracker = self.progress.add_task("running...", total=self.num_tests)

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.num_tests
            ) as executor:
                futures = [
                    executor.submit(self.run_test, test) for test in self.plan.tests
                ]
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        raise e

        self._log_run_end()

        create_markdown_summary(
            self.work_dir, self.plan.tests, list(self.results.values())
        )

        return self.num_failed

    def run_test(self, test):
        target = self.plan.create_target()
        evaluator = self.plan.create_evaluator(
            test=test,
            target=target,
            work_dir=self.work_dir,
        )

        result = evaluator.run()
        if result.success is False:
            self.num_failed += 1

        self.progress.update(self.tracker, advance=1)
        self.results[test.name] = result

    def _log_run_start(self):
        logger.info(
            f"Starting {self.num_tests} tests with max {self.num_threads} workers. Use CTRL+C to exit."
        )

        if self.verbose:
            logger.info(self.plan)

    def _log_run_end(self):
        if self.verbose:
            self._log_test_result()

        self._log_pass_fail_count()
        logger.info(
            f"--- Completed in {round(time.time() - self.start_time, 2)} seconds ---"
        )

    def _log_test_result(self):
        for _, result in self.results.items():
            logger_func = logger.info if result.success else logger.error
            logger_func(
                f"[bold {'green' if result.success else 'red'}]{result.test_name}...{'PASSED' if result.success else 'FAILED'}",
            )

    def _log_pass_fail_count(self):
        passed_count = self.num_tests - self.num_failed
        status_str = (
            f"[red]{passed_count} passed, {self.num_failed} failed"
            if self.num_failed
            else f"[green]{self.num_tests} passed"
        )
        logger_func = logger.error if self.num_failed else logger.info
        logger_func(status_str)
