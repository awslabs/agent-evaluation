import os
from distutils.core import setup

from setuptools import find_packages

VERSION = "0.1.0"

DESCRIPTION = "A LLM-powered framework for testing virtual agents."
AUTHOR = "Amazon Web Services"
EMAIL = "agent-evaluation-oss-core-team@amazon.com"
URL = "https://github.com/awslabs/agent-evaluation"

PACKAGE_DIR = "src"
REQUIRES_PYTHON = ">=3.9"
REQUIREMENTS = [
    "pyyaml~=6.0",
    "boto3>=1.34.20,<2.0",
    "click~=8.0",
    "pydantic>=2.1.0,<3.0",
    "rich>=13.7.0,<14.0",
    "jinja2>=3.1.3,<4.0",
    "jsonpath-ng>=1.6.1,<2.0",
]
DEV_REQUIREMENTS = [
    "flake8",
    "black",
    "isort",
    "pytest",
    "pytest-cov",
    "pytest-mock",
    "mkdocs",
    "mkdocs-material",
    "mkdocstrings[python]",
    "mkdocs-click",
    "bandit",
]

PACKAGE_DATA = {
    "": [
        "templates/**/*",
    ],
}


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="agenteval",
    version=VERSION,
    packages=find_packages(where=PACKAGE_DIR),
    package_dir={"": PACKAGE_DIR},
    package_data=PACKAGE_DATA,
    description=DESCRIPTION,
    long_description=read("README.md"),
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIREMENTS,
    extras_require={"dev": DEV_REQUIREMENTS},
    entry_points={"console_scripts": ["agenteval=agenteval.cli:cli"]},
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
