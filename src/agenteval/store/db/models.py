# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Run(Base):
    __tablename__ = "run"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_time: Mapped[datetime.datetime]
    end_time: Mapped[datetime.datetime]

    # 1:n relationship with tests
    tests: Mapped[List["Test"]] = relationship(back_populates="run")


class Test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    steps: Mapped[str]
    initial_prompt: Mapped[str] = mapped_column(nullable=True)
    max_turns: Mapped[int]
    hook: Mapped[str] = mapped_column(nullable=True)
    start_time: Mapped[datetime.datetime]
    end_time: Mapped[datetime.datetime]
    run_id: Mapped[int] = mapped_column(ForeignKey("run.id"))
    run: Mapped["Run"] = relationship(back_populates="tests")

    # 1:1 relationship with expected
    expected: Mapped["Expected"] = relationship(back_populates="test")

    # 1:1 relationship with test result
    test_result: Mapped["TestResult"] = relationship(back_populates="test")


class Expected(Base):
    __tablename__ = "expected"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation: Mapped[str]
    test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))
    test: Mapped["Test"] = relationship(back_populates="expected")


class TestResult(Base):
    __tablename__ = "test_result"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    result: Mapped[str]
    reasoning: Mapped[str]
    passed: Mapped[bool]
    messages: Mapped[str]
    events: Mapped[str]
    evaluator_input_token_count: Mapped[int]
    evaluator_output_token_count: Mapped[int]
    test_id: Mapped[int] = mapped_column(ForeignKey("test.id"))
    test: Mapped["Test"] = relationship(back_populates="test_result")
