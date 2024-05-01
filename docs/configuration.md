# Configuration

```yaml title="agenteval.yml"
evaluator:
  model: claude-3
target:
  type: bedrock-agent
  bedrock_agent_id: string
  bedrock_agent_alias_id: string
tests:
  retrieve_missing_documents:
    steps:
    - Ask agent for a list of missing documents for claim-006.
    expected_results:
    - The agent returns a list of missing documents.
    initial_prompt: Give me a list of missing documents for claim-006.
    max_turns: 2
    hook: path.to.MyHook
```

`evaluator` _(map)_

Refer to [Evaluators](evaluators/index.md) for the available configurations.

---

`target` _(map)_

Refer to [Targets](targets/index.md) for the available configurations.

---

`tests` _(map)_

A map of test cases, where the test name serves as the key.

---

`steps` _(list of strings)_

The steps to perform for the test.

---

`expected_results` _(list of strings)_

The expected results for the test.

---

`initial_prompt` _(string; optional)_

The first message that is sent to the agent, which starts the conversation. If unspecified, the message will be generated based on the `steps` provided.

---

`max_turns` _(integer; optional)_

The maximum number of user-agent exchanges before the test fails. The default is `2`.

---

`hook` _(string; optional)_

The module path to an evaluation hook. Refer to [Hooks](hooks.md) for more details.

---
