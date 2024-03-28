__version__ = "0.1.0"

import logging
import os

from jinja2 import Environment, PackageLoader
from rich.logging import RichHandler

from .hook import Hook

__all__ = ["Hook"]
_LOG_LEVEL_ENV = "LOG_LEVEL"
_FORMAT = "%(message)s"

logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.basicConfig(
    level=os.environ.get(_LOG_LEVEL_ENV, logging.INFO),
    format=_FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, show_level=False)],
)

jinja_env = Environment(loader=PackageLoader(__name__))
