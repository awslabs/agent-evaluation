# Evaluators

An Evaluator is an agent that evaluates a [Target](../targets/index.md) on a test.

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

### Available Evaluators

- [Anthropic Claude](./bedrock/claude.md)
