import os
from distutils.core import setup

from setuptools import find_packages

DIST_NAME = "agent-evaluation"
VERSION = "0.4.1"
DESCRIPTION = "A generative AI-powered framework for testing virtual agents."
AUTHOR = "Amazon Web Services"
EMAIL = "agent-evaluation-oss-core-team@amazon.com"
URL = "https://awslabs.github.io/agent-evaluation/"
PACKAGE_DIR = "src"
REQUIRES_PYTHON = ">=3.9"
PACKAGE_DATA = {
    "": [
        "templates/**/*",
    ],
}


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name=DIST_NAME,
    version=VERSION,
    packages=find_packages(where=PACKAGE_DIR),
    package_dir={"": PACKAGE_DIR},
    package_data=PACKAGE_DATA,
    description=DESCRIPTION,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    install_requires=read("requirements.txt").splitlines(),
    extras_require={"dev": read("requirements-dev.txt").splitlines()},
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
