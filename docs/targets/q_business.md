# Amazon Q Business

Amazon Q Business is a generative AI–powered assistant that can answer questions, provide summaries, generate content, and securely complete tasks based on data and information in your enterprise systems. For more information, visit the AWS documentation [here](https://docs.aws.amazon.com/amazonq/latest/business-use-dg/what-is.html).

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

`q_business_user_id` *(string; optional)*

The identifier of the Amazon Q user.

---