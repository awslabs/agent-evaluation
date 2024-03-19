## Getting started

To begin, initialize a test plan.

```bash
agenteval init
```

This will create an `agenteval.yaml` file in the current directory.

```yaml
evaluator:
  type: bedrock-claude
  model: claude-sonnet
target:
  type: bedrock-agent
  bedrock_agent_id: null
  bedrock_agent_alias_id: null
tasks:
- name: RetrieveMissingDocuments
  steps:
  - Ask agent for a list of missing documents for claim-006.
  expected_results:
  - The agent returns a list of missing documents for claim-006.
```

If you are testing a Amazon Bedrock agent, update the following `target` configurations:

- `bedrock_agent_id`: The unique identifier of the Amazon Bedrock agent. 
- `bedrock_agent_alias_id`: The alias of the Amazon Bedrock agent.

Update `tasks` with your test cases. Each task must have the following:
   
- `name`: A unique name for the task.
- `steps`: A list of steps you want to perform in your task.
- `expected_results`: A list of expected results for your task.

!!! info
            
    Refer to [Targets](./targets.md) for additional targets and their required configurations.

Once you have updated the test plan, you can run your tests:

```bash
agenteval run
```

The results will be printed in your terminal and a Markdown summary will be available in `agenteval_summary.md`.


## Writing test cases

It is important to be clear and concise when writing your test cases.

```yaml
tasks:
- name: GetOpenClaims
  steps:
  - Ask the agent which claims are open.
  expected_results:
  - The agent returns a list of open claims.
```

If your test cases are complex, consider breaking them down into multiple `steps`, `expected_results`, and/or `tasks`.

### Multi-turn conversations

To test multiple user-agent interactions, you can provide multiple `steps` to orchestrate the interaction.


```yaml
tasks:
- name: GetOpenClaimWithDetails
  steps:
  - Ask the agent which claims are open.
  - Once the agent responds with the list of open claims, ask for the details
    on claim-006.
  expected_results:
  - The agent returns the details on claim-006.
```
  
The maximum number of turns allowed for a conversation is configured using the `max_turns` parameter for the task (defaults to `2` when not specified).
If the number of turns in the conversation reaches the `max_turns` limit, then the task will fail.

### Specify the first user message

By default, the first user message in the task is automatically generated based on the list of `steps`. To override this message, you can specify the `initial_prompt`.

```yaml
tasks:
- name: GetOpenClaimWithDetails
  steps:
  - Ask the agent which claims are open.
  - Once the agent responds with the list of open claims, ask for the details
    on claim-006.
  expected_results:
  - The agent returns the details on claim-006.
  initial_prompt: Can you let me know which claims are open?
```