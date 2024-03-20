# Anthropic Claude

## Prerequisites

The principal must have [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) access for the following models:

- Anthropic Claude 3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`)
- Anthropic Claude (`anthropic.claude-v2:1`)
- Anthropic Claude Instant (`anthropic.claude-instant-v1`)

## Configurations

```yaml
evaluator:
  type: bedrock-claude 
  model:
```

`model` *(string; optional)*

The Claude model to use as the Evaluator. This should be one of:

- `claude-sonnet`
- `claude`
- `claude-instant`

If unspecified, `claude-sonnet` will be used.

---