import concurrent.futures
import logging
from typing import Optional

from rich.progress import Progress

from agenteval.plan import Plan
from agenteval.runner.summary import create_markdown_summary

logger = logging.getLogger(__name__)

_MARKDOWN_SUMMARY_TEMPLATE_PATH = "agenteval_summary.md.j2"


class Runner:
    def __init__(
        self,
        plan: Plan,
        verbose: bool,
        num_threads: Optional[int],
    ):
        self.plan = plan
        self.num_tasks = len(self.plan.tasks)
        self.verbose = verbose
        self.num_threads = num_threads
        if not self.num_threads:
            self.num_threads = self.num_tasks
        self.results = {task.name: None for task in self.plan.tasks}
        self.num_failed = 0

    def run(self):
        logger.info(f"Running {self.num_tasks} tasks")

        with Progress(transient=True) as self.progress:
            self.tracker = self.progress.add_task("running...", total=self.num_tasks)

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.num_tasks
            ) as executor:
                futures = [
                    executor.submit(self.run_task, task) for task in self.plan.tasks
                ]
                for future in futures:
                    thread_status = future.result()
                    if thread_status != "success":
                        executor.shutdown(wait=False, cancel_futures=True)
                        raise Exception(thread_status)

        self._log_task_result()
        self._log_pass_fail_count()
        summary_path = create_markdown_summary(
            self.plan.tasks, list(self.results.values())
        )
        logger.info(f"Summary available at {summary_path}")

        self._exit()

    def run_task(self, task):
        try:
            target = self.plan.create_target()
            evaluator = self.plan.create_evaluator(
                task=task,
                target=target,
            )

            result = evaluator.run()
            if result.success is False:
                self.num_failed += 1

            self.progress.update(self.tracker, advance=1)
            self.results[task.name] = result
            return "success"
        except Exception as e:
            return e

    def _log_task_result(self):
        for _, result in self.results.items():
            logger_func = logger.info if result.success else logger.error
            logger_func(
                f"[bold {'green' if result.success else 'red'}]{result.name}...{'PASSED' if result.success else 'FAILED'}",
            )

    def _log_pass_fail_count(self):
        passed_count = self.num_tasks - self.num_failed
        status_str = (
            f"[red]{passed_count} passed, {self.num_failed} failed"
            if self.num_failed
            else f"[green]{self.num_tasks} passed"
        )
        logger_func = logger.error if self.num_failed else logger.info
        logger_func(status_str)

    def _exit(self):
        exit(1 if self.num_failed else 0)
