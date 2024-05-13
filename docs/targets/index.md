# Targets

A target represents the agent you want to test.

---

## Base configurations

!!! info

    This project uses Boto3's credential resolution chain to determine the AWS credentials to use. Please refer to the
    Boto3 [documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) for more details.

```yaml title="agenteval.yml"
target:
  aws_profile: my-profile
  aws_region: us-west-2
  endpoint_url: my-endpoint-url
  max_retry: 10
```

`aws_profile` _(string; optional)_

A profile name that is used to create a Boto3 session.

---

`aws_region` _(string; optional)_

The AWS region that is used to create a Boto3 session.

---

`endpoint_url` _(string; optional)_

The endpoint URL for the AWS service which is used to construct the Boto3 client.

---

`max_retry` _(integer; optional)_

Configures the Boto3 client with the maximum number of retry attempts allowed. The default is `10`.

---

## Built-in targets

- [Agents for Amazon Bedrock](bedrock_agents.md)
- [Knowledge bases for Amazon Bedrock](bedrock_knowledge_bases.md)
- [Amazon Q for Business](q_business.md)
- [Amazon SageMaker endpoints](sagemaker_endpoints.md)

---