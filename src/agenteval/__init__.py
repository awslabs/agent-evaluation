# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from importlib.metadata import version

import logging
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from rich.logging import RichHandler

from .hook import Hook

__all__ = ["Hook"]
__version__ = version("agent-evaluation")


_LOG_LEVEL_ENV = "LOG_LEVEL"


def configure_logger():
    # supress logs from botocore
    logging.getLogger("botocore").setLevel(logging.CRITICAL)

    # configure logging using rich
    formatter = logging.Formatter("%(message)s", datefmt="[%X]")
    handler = RichHandler(markup=True, show_level=True, rich_tracebacks=True)
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)

    logger.setLevel(os.environ.get(_LOG_LEVEL_ENV, logging.INFO))
    logger.addHandler(handler)


configure_logger()

jinja_env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape(
        disabled_extensions=["jinja"],
        default_for_string=True,
        default=True,
    ),
)
