![GitHub License](https://img.shields.io/github/license/awslabs/agent-evaluation)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

# Agent Evaluation - Weni Fork

> **Note**: This is a fork of the original [Agent Evaluation framework by AWS Labs](https://github.com/awslabs/agent-evaluation). This fork adds support for testing [Weni](https://weni.ai) conversational AI agents while maintaining all the original functionality for AWS services.

Agent Evaluation is a generative AI-powered framework for testing virtual agents.

Internally, Agent Evaluation implements an LLM agent (evaluator) that will orchestrate conversations with your own agent (target) and evaluate the responses during the conversation.

## ✨ Key features

- **🆕 Weni Agent Support**: Built-in support for testing [Weni](https://weni.ai) conversational AI agents through their API and WebSocket interface.
- Built-in support for popular AWS services including [Amazon Bedrock](https://aws.amazon.com/bedrock/), [Amazon Q Business](https://aws.amazon.com/q/business/), and [Amazon SageMaker](https://aws.amazon.com/sagemaker/). You can also [bring your own agent](https://awslabs.github.io/agent-evaluation/targets/custom_targets/) to test using Agent Evaluation.
- Orchestrate concurrent, multi-turn conversations with your agent while evaluating its responses.
- Define [hooks](https://awslabs.github.io/agent-evaluation/hooks/) to perform additional tasks such as integration testing.
- Can be incorporated into CI/CD pipelines to expedite the time to delivery while maintaining the stability of agents in production environments.

## 🚀 Quick Start with Weni

### Installation

1. Clone this repository:
```bash
git clone https://github.com/weni-ai/agent-evaluation.git
cd agent-evaluation
```

2. Install the package and dependencies:
```bash
pip install -e .
# or
pip install -r requirements.txt
```

### Prerequisites for Weni Target

> **⚠️ Important**: You need both AWS and Weni credentials to run evaluations!

To test Weni agents, you'll need:

1. **AWS Credentials**: Required for the evaluator (Claude model via Bedrock)
   - AWS Access Key ID
   - AWS Secret Access Key
   - AWS Session Token

2. **A Weni Project**: An active project in the [Weni platform](https://weni.ai)

3. **Weni Authentication Credentials**:
   - `WENI_PROJECT_UUID`: Your project's unique identifier
   - `WENI_BEARER_TOKEN`: Your authentication bearer token

### Setting up Environment Variables

**macOS/Linux:**
```bash
# AWS Credentials (required for evaluator)
export AWS_ACCESS_KEY_ID="your-aws-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
export AWS_SESSION_TOKEN="your-aws-session-token"

# Weni Credentials (required for target)
export WENI_PROJECT_UUID="your-project-uuid-here"
export WENI_BEARER_TOKEN="your-bearer-token-here"
```

**Windows (Command Prompt):**
```cmd
REM AWS Credentials (required for evaluator)
set AWS_ACCESS_KEY_ID=your-aws-access-key-id
set AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
set AWS_SESSION_TOKEN=your-aws-session-token

REM Weni Credentials (required for target)
set WENI_PROJECT_UUID=your-project-uuid-here
set WENI_BEARER_TOKEN=your-bearer-token-here
```

**Windows (PowerShell):**
```powershell
# AWS Credentials (required for evaluator)
$env:AWS_ACCESS_KEY_ID="your-aws-access-key-id"
$env:AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
$env:AWS_SESSION_TOKEN="your-aws-session-token"

# Weni Credentials (required for target)
$env:WENI_PROJECT_UUID="your-project-uuid-here"
$env:WENI_BEARER_TOKEN="your-bearer-token-here"
```

### Basic Usage

Create a test configuration file `agenteval.yml`:

```yaml
evaluator:
  model: claude-haiku-3_5-us
  aws_region: us-east-1

target:
  type: weni
  timeout: 30      # Optional: max seconds to wait for response

tests:
  greeting:
    steps:
      - Send a greeting "Olá, bom dia!"
      - Ask what "com oq vc pode me ajudar?"
    expected_results:
      - Agent responds with a friendly greeting
      - Agent shows up a menu with options to help the user

  purchase_outside_postal_code:
    steps:
      - Ask information "quero comprar arroz"
      - Give the postal code "04538-132"
    expected_results:
      - Agent responds asking for postal code
      - Agent says it doesn't deliver to this postal code
```

Run the evaluation:

```bash
agenteval run agenteval.yml
```

### Configuration Options for Weni Target

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `type` | string | Yes | - | Must be `"weni"` |
| `timeout` | integer | No | `30` | Max seconds to wait for response |
| `weni_project_uuid` | string | No | - | Project UUID (use env var instead) |
| `weni_bearer_token` | string | No | - | Bearer token (use env var instead) |

### Advanced Example

Here's a more comprehensive test plan:

```yaml
evaluator:
  model: claude-haiku-3_5-us
  aws_region: us-east-1

target:
  type: weni
  timeout: 45

tests:
  # Basic greeting test
  greeting:
    steps:
      - Send a greeting "Olá, como você está?"
    expected_results:
      - Agent responds politely
      - Agent asks how it can help

  # Multi-turn conversation
  product_inquiry:
    steps:
      - Ask "Quais produtos vocês têm?"
      - Follow up with "Qual é o preço do arroz?"
      - Ask "Vocês entregam em São Paulo?"
    expected_results:
      - Agent provides product information
      - Agent gives pricing details
      - Agent confirms delivery area

  # Error handling
  unclear_input:
    steps:
      - Send unclear text "xyz123 !!!"
    expected_results:
      - Agent handles gracefully
      - Agent asks for clarification
      - No error messages shown to user

  # Context maintenance
  context_test:
    steps:
      - Say "Quero comprar feijão"
      - Ask "Qual o prazo de entrega?"
      - Ask "E o frete?"
    expected_results:
      - Agent remembers the product context
      - Agent provides delivery timeframe
      - Agent gives shipping cost information
```

## 📚 Documentation

To get started with the original framework features, please visit the full documentation [here](https://awslabs.github.io/agent-evaluation/). 

For Weni-specific documentation, see the [Weni Target Documentation](docs/targets/weni.md).

To contribute, please refer to [CONTRIBUTING.md](./CONTRIBUTING.md)

## 🔧 Troubleshooting Weni Target

### Common Issues

**AWS Authentication Errors**
- Verify your AWS environment variables are set correctly (ACCESS_KEY_ID, SECRET_ACCESS_KEY, SESSION_TOKEN)
- Ensure you have access to Amazon Bedrock in your specified region
- Check that your AWS credentials have the necessary Bedrock permissions
- Verify the `aws_region` in your configuration matches your AWS account's region access

**Weni Authentication Errors**
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

## 🆚 Differences from Original

This fork maintains full compatibility with the original AWS Labs Agent Evaluation framework while adding:

- **Weni Target Support**: Native integration with Weni conversational AI platform
- **WebSocket Communication**: Real-time bidirectional communication with Weni agents
- **Session Isolation**: Each test case uses unique contact identifiers for proper conversation isolation

All original AWS targets (Bedrock, Q Business, SageMaker, etc.) continue to work exactly as in the original repository.

## 🤝 Contributing

We welcome contributions! This fork follows the same contribution guidelines as the original project. Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

For Weni-specific contributions:
1. Test your changes with actual Weni agents
2. Update the Weni target documentation if needed
3. Ensure backward compatibility with existing configurations

## 👏 Contributors

Shout out to these awesome contributors:

<a href="https://github.com/awslabs/agent-evaluation/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=awslabs/agent-evaluation" />
</a>