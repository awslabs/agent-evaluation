# Home

Agent Evaluation is a LLM-powered framework for testing virtual agents.

## How it works

Agent Evaluation implements an agent ([Evaluator](./evaluators/index.md)) that will orchestrate conversations with your agent ([Target](./targets/index.md)) and evaluate the responses during the conversation.

You simply define your test cases using natural language.

For example:

```yaml
tests:
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

Agent Evaluation requires `python>=3.9`. Please make sure you have an acceptable version of Python before proceeding.

To install:

```bash
pip install agenteval
```

You can also install from source by cloning the [repo](https://github.com/awslabs/agent-evaluation) and installing from the project root.

```bash
pip install .
```
