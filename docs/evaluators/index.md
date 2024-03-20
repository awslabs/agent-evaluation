# Evaluators

An Evaluator is an agent that evaluates a [Target](../targets/index.md) on a task.

## Configurations

```yaml
evaluator:
  aws_profile:
  aws_region:
  endpoint_url:
```

`aws_profile` *(string; optional)*

Named profile used to access AWS services and resources. If unspecified, the `default` profile is used.

---

`aws_region` *(string; optional)*

AWS Region to send requests to. If unspecified, the region associated with the `default` profile is used.

---

`endpoint_url` *(string; optional)*

The endpoint URL for the AWS service. If unspecified, the public endpoint based on `aws_region` will be used.

---