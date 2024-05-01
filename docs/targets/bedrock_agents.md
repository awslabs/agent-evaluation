# Agents for Amazon Bedrock

Agents for Amazon Bedrock offers you the ability to build and configure autonomous agents in your application. For more information, visit the AWS documentation [here](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html).

## Prerequisites

The principal must have the following permissions:

- [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html)

## Configurations

```yaml title="agenteval.yml"
target:
  type: bedrock-agent
  bedrock_agent_id: my-agent-id
  bedrock_agent_alias_id: my-alias-id
```

`bedrock_agent_id` *(string)*

The unique identifier of the Bedrock agent.

---

`bedrock_agent_alias_id` *(string)*

The alias of the Bedrock agent.

---