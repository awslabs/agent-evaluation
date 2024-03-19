# Home

Agent Evaluation is a LLM-powered framework for testing and validating virtual agents.

## How it works

Agent Evaluation implements an agent ([Evaluator](./evaluators.md)) that will orchestrate conversations with your agent ([Target](./targets.md)) and evaluate the responses during the conversation.

You simply define your test cases in the form of tasks, using natural language.

For example:

```yaml
tasks:
- name: CheckClaimStatus
  steps:
  - Ask agent for the status of claim-006
  expected_results:
  - The agent responds the the status is open
- name: CheckPolicyType
  steps:
  - Ask agent for the policy type of claim-006
  expected_results:
  - Agent responds the the policy type is home.
```

## Install

Agent Evaluation requires `python>=3.7`. Please make sure you have an acceptable version of Python before proceeding.


To install:

```bash
pip install agenteval
```


You can also install from source by cloning the [repo](https://gitlab.aws.dev/genai-tooling-incubator/agenteval) and installing from the project root.

```bash
pip install .
```

