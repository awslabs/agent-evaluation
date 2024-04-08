# Anthropic Claude

This evaluator is implemented using [Anthropic's Claude](https://www.anthropic.com/claude) hosted on [Amazon Bedrock](https://aws.amazon.com/bedrock/claude/).

## Prerequisites

The principal must have [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) access for the following models:

- Anthropic Claude 3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`)
- Anthropic Claude 3 Haiku (`anthropic.claude-3-haiku-20240307-v1:0`)
- Anthropic Claude (`anthropic.claude-v2:1`)

## Configurations

```yaml
evaluator:
  type: bedrock-claude
  model:
```

`model` _(string; optional)_

The Claude model to use as the Evaluator. This should be one of following:

- `claude-sonnet`
- `claude-haiku`
- `claude`

If unspecified, `claude-haiku` will be used.

---
