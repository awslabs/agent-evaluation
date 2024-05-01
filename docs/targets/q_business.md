# Amazon Q for Business

Amazon Q is a fully managed, generative-AI powered assistant that you can configure to answer questions, provide summaries, generate content, and complete tasks based on data in your enterprise. For more information, visit the AWS documentation [here](https://docs.aws.amazon.com/amazonq/latest/business-use-dg/what-is.html).


!!! warning

    Amazon Q is in preview release and is subject to change.

## Prerequisites

The principal must have the following permissions:

- [ChatSync](https://docs.aws.amazon.com/amazonq/latest/api-reference/API_ChatSync.html)

## Configurations

```yaml title="agenteval.yml"
target:
  type: q-business
  q_business_application_id: my-app-id
  q_business_user_id: my-user-id
```

`q_business_application_id` *(string)*

The unique identifier of the Amazon Q application.

---

`q_business_user_id` *(string)*

The identifier of the Amazon Q user.

---