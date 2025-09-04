# Weni Agents

Weni is an intelligent agent platform that enables conversational AI experiences. This target allows you to test Weni agents through their API and WebSocket interface.

## Prerequisites

To use the Weni target, you need:

1. **A Weni Project**: An active Weni project with a configured agent
2. **Authentication Credentials**:
   - `WENI_PROJECT_UUID`: Your Weni project's unique identifier
   - `WENI_BEARER_TOKEN`: Your authentication bearer token for the Weni API

These credentials can be provided either:
- As environment variables (recommended for security)
- Directly in the configuration file (not recommended for production)

## Installation

The Weni target requires the `websocket-client` package, which is included in the main requirements:

```bash
pip install -r requirements.txt
```

## Configuration

```yaml title="agenteval.yml"
target:
  type: weni
  language: pt-BR  # Optional, defaults to pt-BR
  timeout: 30      # Optional, max seconds to wait for response
  # Optionally provide credentials directly (not recommended):
  # weni_project_uuid: your-project-uuid
  # weni_bearer_token: your-bearer-token
```

### Parameters

`weni_project_uuid` *(string; optional)*

The unique identifier of your Weni project. If not provided, the target will look for the `WENI_PROJECT_UUID` environment variable.

```yaml
weni_project_uuid: 45718786-4066-4338-9e86-f3ea525224d2
```

---

`weni_bearer_token` *(string; optional)*

The bearer token for authenticating with the Weni API. If not provided, the target will look for the `WENI_BEARER_TOKEN` environment variable.

```yaml
weni_bearer_token: your-bearer-token-here
```

---

`language` *(string; optional)*

The language code for the conversation. This affects how the agent processes and responds to messages. Defaults to `"pt-BR"`.

Common language codes:
- `pt-BR`: Brazilian Portuguese (default)
- `en-US`: American English
- `es`: Spanish
- `fr`: French

```yaml
language: en-US
```

---

`timeout` *(integer; optional)*

Maximum time in seconds to wait for the agent's response via WebSocket. Defaults to `30`.

```yaml
timeout: 45
```

## How It Works

The Weni target interacts with Weni agents through a two-step process:

1. **Message Sending**: Sends the user prompt to the Weni API via HTTP POST request
2. **Response Reception**: Connects to a WebSocket endpoint to receive the agent's asynchronous response

Each test case uses a unique contact identifier (`contact_urn`) to maintain conversation isolation and history throughout the test session.

## Example Test Plan

```yaml title="weni_test_plan.yml"
evaluator:
  model: claude-3

target:
  type: weni
  language: pt-BR
  timeout: 30

tests:
  greeting:
    steps:
      - Send a greeting "Olá, bom dia!"
    expected_results:
      - Agent responds with a friendly greeting
      - Agent introduces itself or explains its capabilities

  product_inquiry:
    steps:
      - Ask "Quais produtos vocês têm disponíveis?"
    expected_results:
      - Agent provides information about available products
      - Response includes clear product descriptions or categories

  multi_turn_conversation:
    steps:
      - Ask "Qual é o horário de funcionamento?"
      - Follow up with "E aos finais de semana?"
    expected_results:
      - Agent provides business hours for weekdays
      - Agent maintains context and provides weekend hours
      - Responses are coherent and contextual

  help_request:
    steps:
      - Say "Preciso de ajuda com um problema"
    expected_results:
      - Agent offers assistance
      - Agent asks clarifying questions about the problem
      - Response is empathetic and helpful

  error_handling:
    steps:
      - Send an unclear message "xyz123 !!!"
    expected_results:
      - Agent handles the unclear input gracefully
      - Agent asks for clarification or provides guidance
      - No error messages are exposed to the user
```

## Running Tests

### Using Environment Variables (Recommended)

```bash
export WENI_PROJECT_UUID="your-project-uuid"
export WENI_BEARER_TOKEN="your-bearer-token"
agenteval run --test-plan weni_test_plan.yml
```

### Using Configuration File

If credentials are provided in the configuration file:

```bash
agenteval run --test-plan weni_test_plan.yml
```

## Troubleshooting

### Common Issues

**Authentication Errors**
- Verify your `WENI_BEARER_TOKEN` is valid and not expired
- Check that the `WENI_PROJECT_UUID` matches your actual project
- Ensure the bearer token has the necessary permissions for the project

**Connection Issues**
- Verify the Weni API endpoints are accessible from your network
- Check for any firewall or proxy settings blocking HTTPS/WSS connections
- Ensure your internet connection is stable

**Timeout Errors**
- Increase the `timeout` parameter if your agent requires more processing time
- Check if the agent is properly configured and active in the Weni platform
- Verify the agent is not stuck in a processing loop

**WebSocket Connection Failures**
- Ensure the `websocket-client` package is properly installed
- Check for any proxy configurations that might interfere with WebSocket connections
- Verify the WebSocket endpoint URL is correct for your project

### Debug Logging

To enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed information about:
- API request/response details
- WebSocket connection status
- Message processing steps
- Error details

## Limitations

- Each test case maintains its own conversation context through a unique contact identifier
- The target waits for the `finalResponse` message type and ignores intermediate processing messages
- Response time depends on the agent's complexity and the Weni platform's processing time

## See Also

- [Custom Targets](custom_targets.md) - Learn how to create your own custom targets
- [Configuration](../configuration.md) - General configuration options
- [User Guide](../user_guide.md) - Complete guide to using Agent Evaluation
