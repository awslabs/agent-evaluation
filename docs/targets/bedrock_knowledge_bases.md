# Knowledge bases for Amazon Bedrock

Knowledge bases for Amazon Bedrock provides you the capability of amassing data sources into a repository of information. With knowledge bases, you can easily build an application that takes advantage of retrieval augmented generation (RAG), a technique in which the retrieval of information from data sources augments the generation of model responses. For more information, visit the AWS documentation [here](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html).

## Prerequisites

The principal must have the following permissions:

- [RetrieveAndGenerate](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_RetrieveAndGenerate.html)

## Configurations

```yaml title="agenteval.yml"
target:
  type: bedrock-knowledgebase
  model_id: my-model-id
  knowledge_base_id: my-kb-id
```

`model_id` *(string)*

The unique identifier of the foundation model used to generate a response.

---

`knowledge_base_id` *(string)*

The unique identifier of the knowledge base that is queried and the foundation model used for generation.

---