# Configuration

```yaml title="agenteval.yml"
evaluator:
target:
tests:
- name:
  steps:
  expected_results:
  initial_prompt:
  max_turns:
  hook:
```

`evaluator` _(map)_

Refer to [Evaluators](evaluators/index.md) for the required configurations.

---

`target` _(map)_

Refer to [Targets](targets/index.md) for the required configurations.

---

`tests` _(list)_

A list of tests. Each test maps with the following fields:

- `name` _(string)_: The name of the test. Must be unique across all `tasks`.
- `steps` _(list of strings)_: The steps to perform for the test.
- `expected_results` _(list of strings)_: The expected results for the test.
- `initial_prompt` _(string; optional)_: The first message that is sent to the agent, which starts the conversation. If unspecified, the message will be generated based on the `steps` provided.
- `max_turns` _(integer; optional)_: The maximum number of user-agent exchanges before the test fails. The default is `2`.
- `hook` _(string; optional)_: The module path to an evaluation hook. Refer to [Hooks](hooks.md) for more details.

---
