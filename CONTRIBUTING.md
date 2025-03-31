# Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional
documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary
information to effectively respond to your bug report or contribution.

## Table of Contents
- [Reporting Bugs/Feature Requests](#report-bugsfeature-requests)
- [Contributing via Pull Requests](#contributing-via-pull-requests)
    - [Best Practices](#best-practices)
    - [Getting Started](#getting-started)
        - [Linting/Formatting](#lintingformatting)
        - [Testing](#testing)
- [Finding Contributions to Work On](#finding-contributions-to-work-on)
- [Code of Conduct](#code-of-conduct)
- [Security Issue Notifications](#security-issue-notifications)
- [Licensing](#licensing)

## Reporting Bugs/Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check existing open, or recently closed, issues to make sure somebody else hasn't already
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A reproducible test case or series of steps
* The version of our code being used
* Any modifications you've made relevant to the bug
* Anything unusual about your environment or deployment


## Contributing via Pull Requests
Contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the `main` branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.


### Best practices
1. Fork the repository.
2. Commit to your fork using clear commit messages that follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
3. Ensure that linting, formatting and tests are are passing *prior* to raising the pull request.
4. If you are introducing new functionality, please commit the appropriate unit tests.
5. Answer any default questions in the pull request interface.
6. Pay attention to any automated CI failures reported in the pull request, and stay involved in the conversation.
7. Update `CHANGELOG.md` with any noteable changes you make. Be sure to add these changes under `Unreleased`.

### Getting Started

We recommend installing the package locally in editable mode for ease of development. To install the package in editable mode along with the development depedencies, run the following:

```bash
pip install -e ".[dev]"
```

#### Linting/Formatting

The tools below are used for linting and formatting the codebase.

- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Black](https://black.readthedocs.io/en/stable/)
- [isort](https://pycqa.github.io/isort/)

To check for linting and formatting issues, you can run the following:

```bash
flake8 src/ &&  black --check src/ && isort src/ --check --diff
```

#### Testing

This project uses [pytest](https://docs.pytest.org/en/8.2.x/) for unit testing, which you can invoke using the following:

```bash
python -m pytest .
```

#### Testing against CLI path

If relevant to the change, confirm that the [CLI path](https://awslabs.github.io/agent-evaluation/cli/) functions as expected.

This can be achieved by:

1. Creating and activate a `venv`
2. Locally install `agent-evaluation` against your local changes via `pip install -e .`
3. Run `agenteval` CLI against your local changes.

## Finding Contributions to Work On
Looking at the existing issues is a great way to find something to contribute on. As our projects, by default, use the default GitHub issue labels, looking for any issues labeled `good first issue` or `help wanted` is a great place to start.


## Code of Conduct
This project has adopted the [Amazon Open Source Code of Conduct](https://aws.github.io/code-of-conduct).
For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq) or contact
opensource-codeofconduct@amazon.com with any additional questions or comments.


## Security Issue Notifications
If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public github issue.


## Licensing

See the [LICENSE](LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.
