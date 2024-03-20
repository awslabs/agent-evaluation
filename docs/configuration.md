# Configuration

```yaml
evaluator:
target:
tasks:
- name:
  steps:
  expected_results:
  initial_prompt:
  max_turns:
```
`evaluator` *(map)*

The evaluator to use for testing. Refer to [Evaluators](./evaluators/index.md) for the required configurations.

---

`target` *(map)*

The agent to test. Refer to [Targets](./targets/index.md) for the required configurations.

---

`tasks` *(list)*

A list of task maps with the following fields:

- `name` *(string)*: The name of the task. Must be unique across all `tasks`.
- `steps` *(list of strings)*: The steps to perform for the task.
- `expected_results` *(list of strings)*: The expected results for the task.
- `initial_prompt` *(string; optional)*: The first message that is sent to the agent, which starts the conversation. If unspecified, the message will be generated  based on the `steps` provided.
- `max_turns` *(integer; optional)*: The maximum number of user-agent exchanges before the task fails. The default is `2`.

---
