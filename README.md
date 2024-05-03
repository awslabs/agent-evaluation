![PyPI - Version](https://img.shields.io/pypi/v/agent-evaluation)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/agent-evaluation)
![GitHub License](https://img.shields.io/github/license/awslabs/agent-evaluation)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

# Agent Evaluation

Agent Evaluation is a generative AI-powered framework for testing virtual agents.

Internally, Agent Evaluation implements an LLM agent (evaluator) that will orchestrate conversations with your own agent (target) and evaluate the responses during the conversation.

## ✨ Key features

- Built-in support for popular AWS services including [Amazon Bedrock](https://aws.amazon.com/bedrock/), [Amazon Q Business](https://aws.amazon.com/q/business/), and [Amazon SageMaker](https://aws.amazon.com/sagemaker/). You can also [bring your own agent](https://awslabs.github.io/agent-evaluation/targets/custom_targets/) to test using Agent Evaluation.
- Orchestrate concurrent, multi-turn conversations with your agent while evaluating its responses.
- Define [hooks](https://awslabs.github.io/agent-evaluation/hooks/) to perform additional tasks such as integration testing.
- Can be incorporated into CI/CD pipelines to expedite the time to delivery while maintaining the stability of agents in production environments.

## 📚 Documentation

To get started, please visit the full documentation [here](https://awslabs.github.io/agent-evaluation/). To contribute, please refer to [CONTRIBUTING.md](./CONTRIBUTING.md)

## 👏 Contributors

Shout out to these awesome contributors:

<a href="https://github.com/awslabs/agent-evaluation/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=awslabs/agent-evaluation" />
</a>