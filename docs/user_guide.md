## Getting started

To begin, initialize a test plan.

```bash
agenteval init
```

This will create a configuration file named `agenteval.yml` in the current directory.

```yaml title="agenteval.yml"
evaluator:
  type: bedrock-claude
target:
  type: bedrock-agent
  bedrock_agent_id: null
  bedrock_agent_alias_id: null
tests:
- name: RetrieveMissingDocuments
  steps:
  - Ask agent for a list of missing documents for claim-006
  expected_results:
  - The agent returns a list of missing documents.
```

If you are testing an Amazon Bedrock agent, update the following `target` configurations:

- `bedrock_agent_id`: The unique identifier of the Amazon Bedrock agent.
- `bedrock_agent_alias_id`: The alias of the Amazon Bedrock agent.

!!! note
    Refer to [Targets](targets/index.md) for all available configurations.


Update `tests` with your test cases. Each test must have the following:

- `name`: A unique name for the test.
- `steps`: A list of steps you want to perform in your test.
- `expected_results`: A list of expected results for your test.

Once you have updated the test plan, you can run your tests:

!!! warning
    The default [Evaluator](evaluators/index.md) is powered by an Anthropic Claude model from Amazon Bedrock. The charges you incur from using Amazon Bedrock will be your responsibility. **Please review [this page](evaluators/bedrock.md) on Evaluator costs before running your tests.**

```bash
agenteval run
```

The results will be printed in your terminal and a Markdown summary will be available in `agenteval_summary.md`.

You will also find traces saved under `agenteval_traces/`. This is useful for understanding the
flow of evaluation.


## Writing test cases

It is important to be clear and concise when writing your test cases.

```yaml title="agenteval.yml"
tests:
- name: GetOpenClaims
  steps:
  - Ask the agent which claims are open.
  expected_results:
  - The agent returns a list of open claims.
```

If your test case is complex, consider breaking it down into multiple, smaller `tests`.

### Multi-turn conversations

To test multiple user-agent interactions, you can provide multiple `steps` to orchestrate the interaction.

```yaml title="agenteval.yml"
tests:
- name: GetOpenClaimsWithDetails
  steps:
  - Ask the agent which claims are open.
  - Ask the agent for details on claim-006.
  expected_results:
  - The agent returns a list of open claims.
  - The agent returns the details on claim-006.
```

The maximum number of turns allowed for a conversation is configured using the `max_turns` parameter for the test (defaults to `2` when not specified).
If the number of turns in the conversation reaches the `max_turns` limit, then the test will fail.

### Providing data

You can test an agent's ability to prompt the user for data when you include it within the step. For example:

```yaml title="agenteval.yml"
tests:
- name: GetAutoOpenClaims
  steps:
  - Ask the agent which claims are open.
    When the agent asks for the claim type, respond with "Auto".
  expected_results:
  - The agent returns claim-001 and claim-002
```

### Specify the first user message

By default, the first user message in the test is automatically generated based on the first step. To override this message, you can specify the `initial_prompt`.

```yaml title="agenteval.yml"
tests:
- name: GetClaimsWithMissingDocuments
  steps:
  - Ask agent which claims still have missing documents.
  initial_prompt: Can you let me know which claims still have missing documents?
  expected_results:
  - The agent returns claim-003 and claim-004
```
