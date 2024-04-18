# Evaluators

An Evaluator is an agent that evaluates a [Target](../targets/index.md) on a test. The diagram below depicts the workflow used during evaluation.

``` mermaid
graph TD
  A((Start)) --> B{Initial<br>prompt?}
  B -->|yes| C(Invoke agent)
  B -->|no| D(Generate initial prompt)
  D --> C
  C --> E(Get test status)
  E --> F{All steps<br>attempted?}  
  F --> |yes| G(Evaluate conversation)
  F --> |no| H{Max turns<br>reached?}
  H --> |yes| I(Fail)
  style I stroke:#f00
  H --> |no| J(Generate user response)
  J --> C
  G --> K{All expected<br>results<br>observed?}
  K --> |yes| L(Pass)
  style L stroke:#0f0
  K --> |no| I(Fail)
  I --> M((End))
  L --> M
```

---

## Evaluators powered by Amazon Bedrock

### Base configurations

```yaml
evaluator:
  aws_profile:
  aws_region:
  endpoint_url:
```

`aws_profile` _(string; optional)_

Named profile used to access AWS services and resources. If unspecified, the `default` profile is used.

---

`aws_region` _(string; optional)_

AWS Region to send requests to. If unspecified, the region associated with the `default` profile is used.

---

`endpoint_url` _(string; optional)_

The endpoint URL for the AWS service. If unspecified, the public endpoint based on `aws_region` will be used.

---

`max_retry` _(integer; optional)_

The maximum number of retry attempts. The default is `10`.

---

### Available Evaluators

- [Anthropic Claude](./bedrock/claude.md)
