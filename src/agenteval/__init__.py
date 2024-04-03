__version__ = "0.1.0"

import logging
import os

from jinja2 import Environment, PackageLoader
from rich.logging import RichHandler

from .hook import Hook

__all__ = ["Hook"]

_LOG_LEVEL_ENV = "LOG_LEVEL"


def configure_logger():
    # supress logs from botocore
    logging.getLogger("botocore").setLevel(logging.CRITICAL)

    # configure logging using rich
    formatter = logging.Formatter("%(message)s", datefmt="[%X]")
    handler = RichHandler(markup=True, show_level=True)
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)

    logger.setLevel(os.environ.get(_LOG_LEVEL_ENV, logging.INFO))
    logger.addHandler(handler)


configure_logger()

jinja_env = Environment(loader=PackageLoader(__name__))
