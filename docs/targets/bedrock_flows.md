# Amazon Bedrock Flows

Amazon Bedrock Flows offer the ability to link prompts, foundation models, and other AWS services into end-to-end workflows through a graphical UI. For more information, visit the AWS documentation [here](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html).


## Prerequisites

The principal must have the following permissions:

- [InvokeFlow](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeFlow.html)


## Configurations

```yaml title="agenteval.yml"
target:
  type: bedrock-flow
  bedrock_flow_id: my-flow-id
  bedrock_flow_alias_id: my-alias-id
```

`bedrock_flow_id` *(string)*

The unique identifier of the Bedrock flow. Typically 10 characters uppercase alphanumeric.

---

`bedrock_flow_alias_id` *(string)*

The alias of the Bedrock flow. Typically 10 characters uppercase alphanumeric.
