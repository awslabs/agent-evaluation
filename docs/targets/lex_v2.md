# Amazon Lex v2

Amazon Lex V2 is an AWS service for building conversational interfaces for applications using voice and text. Amazon Lex V2 provides the deep functionality and flexibility of natural language understanding (NLU) and automatic speech recognition (ASR) so you can build highly engaging user experiences with lifelike, conversational interactions, and create new categories of products. For more information, visit the AWS documentation [here](https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html).

## Prerequisites

The principal must have the following permissions:

- [RecognizeText](https://docs.aws.amazon.com/lexv2/latest/APIReference/API_runtime_RecognizeText.html)

## Configurations

```yaml title="agenteval.yml"
target:
  type: lex-v2
  bot_id: my-bot-id
  bot_alias_id: my-bot-alias-id
  locale_id: my-locale-id
```

`bot_id` *(string)*

The unique identifier of the Amazon Lex v2 chatbot.

---

`bot_alias_id` *(string; optional)*

The alias of the Amazon Lex v2 chatbot.

---

`locale_id` *(string; optional)*

The locale of the Amazon Lex v2 chatbot.

---