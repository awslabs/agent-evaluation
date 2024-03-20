# Targets

A Target represents the agent to test.

## Configurations

```yaml
target:
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