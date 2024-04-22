# Targets

A Target represents the agent you want to test.

---

## Base configurations

```yaml title="agenteval.yml"
target:
  aws_profile:
  aws_region:
  endpoint_url:
  max_retry:
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

## Built-in Targets

- [Agents for Amazon Bedrock](bedrock_agents.md)
- [Knowledge bases for Amazon Bedrock](bedrock_knowledgebases.md)
- [Amazon Q for Business](q_business.md)
- [Amazon SageMaker endpoints](sagemaker_endpoints.md)

---
