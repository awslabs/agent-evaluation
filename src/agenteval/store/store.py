# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
from typing import Optional

import sqlalchemy
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

import agenteval.environment_variables as env
from agenteval.run import Run
from agenteval.store.db import models
from agenteval.store.db.utils import (
    create_engine,
    init_db_tables,
    is_new_db,
    verify_db_schema,
)
from agenteval.store.defaults import SQLITE_BACKEND_STORE_URL
from agenteval.store.exceptions import NoRecordFoundError
from agenteval.store.return_types import DescribeRun, DescribeTest, ListRuns, ListTests
from agenteval.utils import calculate_pass_rate


class Store:
    """Defines a database store.

    Attributes:
        engine (sqlalchemy.engine.Engine): A SQLAlchemy Engine.
    """

    def __init__(
        self,
        backend_store_url: Optional[str],
        init_tables: bool = True,
        verify_schema: bool = True,
    ):
        """Initialize a database store.

        Args:
            backend_store_url (str): The database URL of the backend store.
            init_tables (bool): Whether to initialize the database tables. Defaults to True.
            verify_schema (bool): Whether to verify the database schema. Defaults to True.
        """
        self.engine = create_engine(
            db_url=Store._resolve_backend_store_url(backend_store_url)
        )

        if is_new_db(self.engine) and init_tables:
            init_db_tables(self.engine)

        if verify_schema:
            verify_db_schema(self.engine)

    def save_run(self, run: Run) -> int:
        """Save a run to the store.

        Args:
            run: (Run): The test plan execution.

        Returns:
            int: The run ID.
        """

        with Session(self.engine) as session:
            run = models.Run(
                start_time=run.start_time,
                end_time=run.end_time,
                tests=[
                    models.Test(
                        name=test.name,
                        steps=json.dumps(test.steps),
                        expected=models.Expected(
                            conversation=json.dumps(test.expected.conversation)
                        ),
                        initial_prompt=test.initial_prompt,
                        max_turns=test.max_turns,
                        hook=test.hook,
                        start_time=test.start_time,
                        end_time=test.end_time,
                        test_result=models.TestResult(
                            result=test.test_result.result,
                            reasoning=test.test_result.reasoning,
                            passed=test.test_result.passed,
                            messages=json.dumps(test.test_result.messages),
                            events=json.dumps(test.test_result.events, default=str),
                            evaluator_input_token_count=test.test_result.evaluator_input_token_count,
                            evaluator_output_token_count=test.test_result.evaluator_output_token_count,
                        ),
                    )
                    for test in run.tests
                ],
            )
            session.add(run)
            session.commit()

            run_id = run.id

        return run_id

    def list_runs(self, max_items: int) -> ListRuns:
        """List runs in the store.

        Args:
            max_items (int): The maximum number of items to return.

        Returns:
            return_types.ListRuns
        """

        with Session(self.engine) as session:
            stmt = (
                select(
                    models.Run.id,
                    models.Run.start_time,
                    models.Run.end_time,
                )
                .order_by(models.Run.end_time.desc())
                .limit(max_items)
            )
            results = session.execute(stmt).all()

        if len(results) == 0:
            raise NoRecordFoundError

        return ListRuns(
            runs=[
                ListRuns.Run(
                    id=r[0],
                    start_time=r[1],
                    end_time=r[2],
                )
                for r in results
            ]
        )

    def list_tests(self, run_id: str, max_items: int) -> ListTests:
        """List tests from a run in the store.

        Args:
            run_id: (str): The run identifier.
            max_items (int): The maximum number of items to return.

        Returns:
            return_types.ListTests
        """
        with Session(self.engine) as session:
            stmt = (
                select(
                    models.Test.name,
                    models.Test.start_time,
                    models.Test.end_time,
                )
                .filter(models.Test.run_id == run_id)
                .order_by(models.Test.name.asc())
                .limit(max_items)
            )

            results = session.execute(stmt).all()

        if len(results) == 0:
            raise NoRecordFoundError

        return ListTests(
            tests=[
                ListTests.Test(name=r[0], start_time=r[1], end_time=r[2])
                for r in results
            ]
        )

    def describe_run(self, run_id: str) -> DescribeRun:
        """Describe a run in the store.

        Args:
            run_id: (str): The run identifier.

        Returns:
            return_types.DescribeRun
        """

        with Session(self.engine) as session:
            stmt = (
                select(
                    models.Run.id,
                    models.Run.start_time,
                    models.Run.end_time,
                    func.count(1),
                    func.sum(
                        case(
                            (
                                models.TestResult.passed == True,  # noqa: E712
                                1,
                            ),
                            (
                                models.TestResult.passed == False,  # noqa: E712
                                0,
                            ),
                        )
                    ),
                    func.sum(models.TestResult.evaluator_input_token_count),
                    func.sum(models.TestResult.evaluator_output_token_count),
                )
                .select_from(models.Run)
                .join(models.Test)
                .join(models.TestResult)
                .filter(models.Run.id == run_id)
            )
            results = session.execute(stmt).one()

        if results[0] is None:
            raise NoRecordFoundError

        return DescribeRun(
            id=results[0],
            start_time=results[1],
            end_time=results[2],
            num_tests=results[3],
            pass_rate=calculate_pass_rate(results[4], results[3]),
            evaluator_input_token_count=results[5],
            evaluator_output_token_count=results[6],
        )

    def describe_test(self, test_name: str, run_id: str) -> DescribeTest:
        """Describe a test in the store.

        Args:
            test_name: (str): The name of the test.
            run_id: (str): The run identifier.

        Returns:
            return_types.DescribeTest
        """
        try:
            with Session(self.engine) as session:
                stmt = (
                    select(models.Test, models.Expected, models.TestResult)
                    .select_from(models.Test)
                    .join(models.Expected)
                    .join(models.TestResult)
                    .filter(models.Test.name == test_name)
                    .filter(models.Test.run_id == run_id)
                )
                test_model, expected_model, test_result_model = session.execute(
                    stmt
                ).one()
        except sqlalchemy.exc.NoResultFound:
            raise NoRecordFoundError

        return DescribeTest(
            name=test_model.name,
            steps=json.loads(test_model.steps),
            expected=DescribeTest.Expected(
                conversation=json.loads(expected_model.conversation)
            ),
            initial_prompt=test_model.initial_prompt,
            max_turns=test_model.max_turns,
            hook=test_model.hook,
            start_time=test_model.start_time,
            end_time=test_model.end_time,
            test_result=DescribeTest.TestResult(
                result=test_result_model.result,
                reasoning=test_result_model.reasoning,
                passed=test_result_model.passed,
                messages=json.loads(test_result_model.messages),
                events=json.loads(test_result_model.events),
                evaluator_input_token_count=test_result_model.evaluator_input_token_count,
                evaluator_output_token_count=test_result_model.evaluator_output_token_count,
            ),
        )

    @staticmethod
    def _resolve_backend_store_url(backend_store_url: Optional[str]) -> str:
        return (
            backend_store_url
            or env.AGENTEVAL_BACKEND_STORE_URL  # noqa: W503
            or SQLITE_BACKEND_STORE_URL  # noqa: W503
        )
