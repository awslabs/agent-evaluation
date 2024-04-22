# Home

Agent Evaluation is a generative AI-powered framework for testing virtual agents.

Internally, Agent Evaluation implements an LLM agent ([Evaluator](evaluators/index.md)) that will orchestrate conversations with your own agent ([Target](targets/index.md)) and evaluate the responses during the conversation.

## Key features

- Built-in support for popular AWS services including [Amazon Bedrock](https://aws.amazon.com/bedrock/), [Amazon Q Business](https://aws.amazon.com/q/business/), and [Amazon SageMaker](https://aws.amazon.com/sagemaker/). You can also [bring their own agents](targets/custom_targets.md) to test using Agent Evaluation.
- Orchestrate concurrent, multi-turn conversations with your agent while evaluating its responses.
- Define [hooks](hooks.md) to perform additional tasks such as integration testing.
- Can be incorporated into CI/CD pipelines to expedite the time to delivery while maintaining the stability of agents in production environments.

---

<div class="grid cards" markdown>

-   :material-rocket-launch-outline:{ .lg .middle } __Getting started__

    ---

    Create your first test using Agent Evaluation.

    [:octicons-arrow-right-24: User Guide](user_guide.md#getting-started)

-   :material-target:{ .lg .middle } __Built-in Targets__

    ---

    View the required configurations for your agent.

    [:octicons-arrow-right-24: Targets](targets/index.md)

-   :material-pencil-outline:{ .lg .middle } __Writing test cases__

    ---

    Learn how to write test cases in Agent Evaluation.

    [:octicons-arrow-right-24: User Guide](user_guide.md#writing-test-cases)

-   :material-github:{ .lg .middle } __Contribute__

    ---
    Review the contributing guidelines to get started!

    [:octicons-arrow-right-24: GitHub](https://github.com/awslabs/agent-evaluation/blob/main/CONTRIBUTING.md)


</div>