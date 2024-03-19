An Evaluator is an agent that evaluates a [Target](./targets.md) on a task.

---

## Evaluators on AWS

### Configurations

```yaml
evaluator:
  aws_profile:
  aws_region:
  endpoint_url:
```

- `aws_profile` *(string; optional)*: Named profile used to access AWS services and resources. If unspecified, the `default` profile is used.
- `aws_region` *(string; optional)*: AWS Region to send requests to. If unspecified, the region associated with the `default` profile is used.
- `endpoint_url` *(string; optional)*:  The endpoint URL for the AWS service. If unspecified, the public endpoint based on `aws_region` will be used.

### Claude on Amazon Bedrock

#### Prerequisites

The principal must have [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) access for the following models:

- Anthropic Claude 3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`)
- Anthropic Claude (`anthropic.claude-v2:1`)
- Anthropic Claude Instant (`anthropic.claude-instant-v1`)

#### Configurations

```yaml
  type: bedrock-claude 
  model:
```

- `model` *(string; optional)*: The Claude model to use as the Evaluator. This should be one of:
    - `claude-sonnet`
    - `claude`
    - `claude-instant`

    If unspecified, `claude-sonnet` will be used.

---

## Custom Evaluators

Example coming soon!