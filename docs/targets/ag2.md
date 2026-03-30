# AG2

[AG2](https://ag2.ai/) (formerly AutoGen) is an open-source multi-agent framework for building AI agent systems. For more information, visit the AG2 documentation [here](https://docs.ag2.ai/).

## Prerequisites

- `ag2` package installed: `pip install ag2[openai]`
- API key for your LLM provider (e.g., OpenAI, Azure, Amazon Bedrock)

## Configurations

```yaml title="agenteval.yml"
target:
  type: ag2
  model: gpt-4o-mini
  api_type: openai
  system_message: "You are a helpful customer support agent."
  max_turns: 3
```

`model` *(string; optional)*

The LLM model to use. Defaults to `gpt-4o-mini`.

---

`api_type` *(string; optional)*

The API type. Defaults to `openai`. Supported values include `openai`, `bedrock`, `mistral`, and others supported by AG2.

---

`api_key` *(string; optional)*

The API key for the LLM provider. Reads from the `OPENAI_API_KEY` environment variable if not provided.

---

`system_message` *(string; optional)*

The system message for the assistant agent. Defaults to `"You are a helpful AI assistant."`.

---

`max_turns` *(integer; optional)*

The maximum number of consecutive auto replies. Defaults to `3`.

## Environment Variables

Set your API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-your-key-here
```

## Examples

### OpenAI

```yaml title="agenteval.yml"
target:
  type: ag2
  model: gpt-4o-mini
  api_type: openai
  system_message: "You are a travel booking assistant."
  max_turns: 5
```

### Amazon Bedrock

AG2 supports Amazon Bedrock natively:

```yaml title="agenteval.yml"
target:
  type: ag2
  model: anthropic.claude-3-sonnet-20240229-v1:0
  api_type: bedrock
```
