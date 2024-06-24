# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from typing import Optional

import sqlalchemy
from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.engine import Engine

from agenteval.store.db.models import Run
from agenteval.store.exceptions import SchemaAlreadyUpToDateError, SchemaOutdatedError

logger = logging.getLogger(__name__)


def create_engine(db_url: Optional[str]) -> Engine:
    """Create a SQLAlchemy Engine instance from a database URL.

    Args:
        db_url (str): A database URL.

    Returns:
        Engine: A SQLAlchemy Engine.
    """

    return sqlalchemy.create_engine(db_url, echo=False)


def is_new_db(engine: Engine) -> bool:
    """Check if database is new based on the existence of
    the run table.

    Args:
        engine: A SQLAlchemy Engine.

    Returns:
        bool: True if new, False otherwise.
    """

    return Run.__tablename__ not in sqlalchemy.inspect(engine).get_table_names()


def init_db_tables(engine: Engine):
    """Initialize the tables in the database.

    Args:
        engine: A SQLAlchemy Engine.
    """
    logger.info("Creating initial database tables...")
    upgrade_db_schema(engine)


def verify_db_schema(engine: Engine):
    """Check if current revision that exists in the database
    matches the head revision.

    Args:
        engine: A SQLAlchemy Engine.

    Raises:
        DatabaseSchemaOutdated: If the current revision is not the head revision.
    """
    head = _get_head_revision()
    current = _get_current_revision(engine)

    if head != current:
        raise SchemaOutdatedError(current_revision=current, head_revision=head)


def upgrade_db_schema(engine: Engine):
    """Upgrade the database to the head revision.

    Args:
        engine: A SQLAlchemy Engine.

    Raises:
        SchemaAlreadyUpToDateError: If the current revision is already the head revision.
    """

    head = _get_head_revision()
    current = _get_current_revision(engine)

    if head == current:
        raise SchemaAlreadyUpToDateError()

    config = _get_alembic_config(db_url=str(engine.url))

    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")


def _get_current_revision(engine: Engine) -> str:
    """Get the current revision that exists in the
    database.
    """
    with engine.connect() as connection:
        mc = MigrationContext.configure(connection)
        return mc.get_current_revision()


def _get_head_revision() -> str:
    """Get the head revision."""
    config = _get_alembic_config(db_url="")
    script = ScriptDirectory.from_config(config)
    heads = script.get_heads()
    return heads[0]


def _get_alembic_config(db_url: str) -> Config:
    """Fetch the alembic config used for migration."""
    alembic_dir = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "migrations")
    )

    db_url = db_url.replace("%", "%%")
    config = Config(os.path.join(alembic_dir, "alembic.ini"))
    config.set_main_option("script_location", alembic_dir)
    config.set_main_option("sqlalchemy.url", db_url)
    return config
