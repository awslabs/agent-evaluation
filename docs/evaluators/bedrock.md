# Amazon Bedrock

Evaluators that leverage foundation models on [Amazon Bedrock](https://aws.amazon.com/bedrock/).

!!! note

    These Evaluators directly utilize the available foundation models. They do not make use of the [Agents for Amazon Bedrock](https://aws.amazon.com/bedrock/agents/) functionality.

## Costs

Evaluators on Amazon Bedrock utilizes the [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) API with On-Demand mode, which will incur AWS charges based on input and output tokens processed. You can find the latest pricing details for Amazon Bedrock [here](https://aws.amazon.com/bedrock/pricing/). 

The cost of running an Evaluator for a single test is influenced by the following:

1. The number and length of the steps.
2. The number and length of expected results.
3. The length of the target agent's responses.

## Anthropic Claude

This evaluator is implemented using [Anthropic's Claude](https://www.anthropic.com/claude) on [Amazon Bedrock](https://aws.amazon.com/bedrock/claude/).

### Prerequisites

The principal must have [InvokeModel](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html) access for the following models:

- Anthropic Claude 3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`)
- Anthropic Claude 3 Haiku (`anthropic.claude-3-haiku-20240307-v1:0`)
- Anthropic Claude (`anthropic.claude-v2:1`)

### Configurations

```yaml title="agenteval.yml"
evaluator:
  type: bedrock-claude
  model:
```

`model` _(string; optional)_

The Claude model to use as the Evaluator. This should be one of following:

- `claude-sonnet`
- `claude-haiku`
- `claude`

If unspecified, `claude-sonnet` will be used.

---